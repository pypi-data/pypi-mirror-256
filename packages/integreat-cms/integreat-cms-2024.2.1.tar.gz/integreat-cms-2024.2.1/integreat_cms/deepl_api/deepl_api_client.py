from __future__ import annotations

import logging
from html import unescape
from typing import TYPE_CHECKING

import deepl
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from ..core.utils.machine_translation_api_client import MachineTranslationApiClient
from ..core.utils.machine_translation_provider import MachineTranslationProvider
from ..textlab_api.utils import check_hix_score

if TYPE_CHECKING:
    from django.forms.models import ModelFormMetaclass
    from django.http import HttpRequest

    from integreat_cms.cms.models.events.event import Event
    from integreat_cms.cms.models.events.event_translation import EventTranslation
    from integreat_cms.cms.models.languages.language import Language
    from integreat_cms.cms.models.pages.page import Page
    from integreat_cms.cms.models.pages.page_translation import PageTranslation
    from integreat_cms.cms.models.pois.poi import POI
    from integreat_cms.cms.models.pois.poi_translation import POITranslation
    from integreat_cms.cms.models.regions.region import Region

logger = logging.getLogger(__name__)


class DeepLApiClient(MachineTranslationApiClient):
    """
    DeepL API client to automatically translate selected objects.
    """

    def __init__(self, request: HttpRequest, form_class: ModelFormMetaclass) -> None:
        """
        Initialize the DeepL client

        :param region: The current region
        :param form_class: The :class:`~integreat_cms.cms.forms.custom_content_model_form.CustomContentModelForm`
                           subclass of the current content type
        """
        super().__init__(request, form_class)
        if not MachineTranslationProvider.is_permitted(
            request.region, request.user, form_class._meta.model
        ):
            raise RuntimeError(
                f'Machine translations are disabled for content type "{form_class._meta.model}" and {request.user!r}.'
            )
        if not settings.DEEPL_ENABLED:
            raise RuntimeError("DeepL is disabled globally.")
        self.translator = deepl.Translator(
            auth_key=settings.DEEPL_AUTH_KEY, server_url=settings.DEEPL_API_URL
        )
        self.translatable_attributes = ["title", "content", "meta_description"]

    @staticmethod
    def get_target_language_key(target_language: Language) -> str:
        """
        This function decides the correct target language key

        :param target_language: the target language
        :return: target_language_key which is 2 characters long for all languages except English and Portugese where the BCP tag is transmitted
        """
        deepl_config = apps.get_app_config("deepl_api")
        for code in [target_language.slug, target_language.bcp47_tag]:
            if code.lower() in deepl_config.supported_target_languages:
                return code
        return ""

    def check_usage(
        self,
        region: Region,
        source_translation: EventTranslation | (PageTranslation | POITranslation),
    ) -> tuple[bool, int]:
        """
        This function checks if the attempted translation would exceed the region's word limit

        :param region: region for which to check usage
        :param source_translation: single content object
        :return: translation would exceed limit, region budget, attempted translation word count
        """
        # Gather content to be translated and calculate total word count
        attributes = [
            getattr(source_translation, attr, None)
            for attr in self.translatable_attributes
        ]
        content_to_translate = [
            unescape(strip_tags(attr)) for attr in attributes if attr
        ]

        content_to_translate_str = " ".join(content_to_translate)
        for char in "-;:,;!?\n":
            content_to_translate_str = content_to_translate_str.replace(char, " ")
        word_count = len(content_to_translate_str.split())

        # Check if translation would exceed DeepL usage limit
        region.refresh_from_db()
        # Allow up to DEEPL_SOFT_MARGIN more words than the actual limit
        word_count_leeway = max(1, word_count - settings.DEEPL_SOFT_MARGIN)
        translation_exceeds_limit = region.deepl_budget_remaining < word_count_leeway

        return (translation_exceeds_limit, word_count)

    def translate_queryset(
        self, queryset: list[Event] | (list[Page] | list[POI]), language_slug: str
    ) -> None:
        """
        This function translates a content queryset via DeepL

        :param queryset: The content QuerySet
        :param language_slug: The target language slug
        """
        with transaction.atomic():
            # Re-select the region from db to prevent simultaneous
            # requests exceeding the DeepL usage limit
            region = (
                apps.get_model("cms", "Region")
                .objects.select_for_update()
                .get(id=self.request.region.id)
            )
            # Get target language
            target_language = region.get_language_or_404(language_slug)
            source_language = region.get_source_language(language_slug)

            target_language_key = self.get_target_language_key(target_language)

            for content_object in queryset:
                source_translation = content_object.get_translation(
                    source_language.slug
                )
                if not source_translation:
                    messages.error(
                        self.request,
                        _('No source translation could be found for {} "{}".').format(
                            type(content_object)._meta.verbose_name.title(),
                            content_object.best_translation.title,
                        ),
                    )
                    continue

                if not check_hix_score(self.request, source_translation):
                    continue

                existing_target_translation = content_object.get_translation(
                    target_language.slug
                )

                # Before translating, check if translation would exceed usage limit
                (
                    translation_exceeds_limit,
                    word_count,
                ) = self.check_usage(region, source_translation)
                if translation_exceeds_limit:
                    messages.error(
                        self.request,
                        _(
                            "Translation from {} to {} not possible: translation of {} words would exceed the remaining budget of {} words."
                        ).format(
                            source_language,
                            target_language,
                            word_count,
                            region.deepl_budget_remaining,
                        ),
                    )
                    continue

                data = {
                    "status": (
                        existing_target_translation.status
                        if existing_target_translation
                        else source_translation.status
                    ),
                    "machine_translated": True,
                    "currently_in_translation": False,
                }

                for attr in self.translatable_attributes:
                    # Only translate existing, non-empty attributes
                    if hasattr(source_translation, attr) and getattr(
                        source_translation, attr
                    ):
                        # data has to be unescaped for DeepL to recognize Umlaute
                        data[attr] = self.translator.translate_text(
                            unescape(getattr(source_translation, attr)),
                            source_lang=source_language.slug,
                            target_lang=target_language_key,
                            tag_handling="html",
                        )

                content_translation_form = self.form_class(
                    data=data,
                    instance=existing_target_translation,
                    additional_instance_attributes={
                        "creator": self.request.user,
                        "language": target_language,
                        source_translation.foreign_field(): content_object,
                    },
                )
                # Validate event translation
                if content_translation_form.is_valid():
                    content_translation_form.save()
                    # Revert "currently in translation" value of all versions
                    if existing_target_translation:
                        if settings.REDIS_CACHE:
                            existing_target_translation.all_versions.invalidated_update(
                                currently_in_translation=False
                            )
                        else:
                            existing_target_translation.all_versions.update(
                                currently_in_translation=False
                            )

                    logger.debug(
                        "Successfully translated for: %r",
                        content_translation_form.instance,
                    )
                    messages.success(
                        self.request,
                        _('{} "{}" has successfully been translated ({} ➜ {}).').format(
                            type(content_object)._meta.verbose_name.title(),
                            source_translation.title,
                            source_language,
                            target_language,
                        ),
                    )
                else:
                    logger.error(
                        "Automatic translation for %r could not be created because of %r",
                        content_object,
                        content_translation_form.errors,
                    )
                    messages.error(
                        self.request,
                        _('{} "{}" could not be translated automatically.').format(
                            type(content_object)._meta.verbose_name.title(),
                            source_translation.title,
                        ),
                    )

                # Update remaining DeepL usage for the region
                region.deepl_budget_used += word_count
                region.save()
