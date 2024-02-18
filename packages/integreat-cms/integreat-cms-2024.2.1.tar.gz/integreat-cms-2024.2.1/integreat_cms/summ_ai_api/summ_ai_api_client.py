"""
This module contains the API client to interact with the SUMM.AI API
"""

from __future__ import annotations

import asyncio
import logging
from itertools import chain
from typing import TYPE_CHECKING

import aiohttp
from django.conf import settings

from ..core.utils.machine_translation_api_client import MachineTranslationApiClient
from ..core.utils.machine_translation_provider import MachineTranslationProvider
from .utils import TranslationHelper

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from typing import Iterator

    from aiohttp import ClientSession
    from django.forms.models import ModelFormMetaclass
    from django.http import HttpRequest

    from ..cms.models.pages.page import Page
    from .utils import TextField

logger = logging.getLogger(__name__)


class SummAiException(Exception):
    """
    Custom Exception class for errors during interaction with SUMM.AI
    """


class SummAiApiClient(MachineTranslationApiClient):
    """
    SUMM.AI API client to get German pages in Easy German language.
    """

    def __init__(self, request: HttpRequest, form_class: ModelFormMetaclass) -> None:
        """
        Constructor initializes the class variables

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
        if not settings.SUMM_AI_ENABLED:
            raise RuntimeError("SUMM.AI is disabled globally.")
        if not self.region.summ_ai_enabled:
            raise RuntimeError(f"SUMM.AI is disabled in {self.region!r}.")

    async def translate_text_field(
        self, session: ClientSession, text_field: TextField
    ) -> TextField:
        """
        Uses :meth:`aiohttp.ClientSession.post` to perform an asynchronous POST request to the SUMM.AI API.
        After the translation is finished, the processing is delegated to the specific textfield's
        :meth:`~integreat_cms.summ_ai_api.utils.TextField.translate`.

        :param session: The session object which is used for the request
        :param text_field: The text field to be translated
        :return: The modified text field containing the translated text
        """
        logger.debug("Translating %r", text_field)
        # Use test region for development
        user = settings.TEST_REGION_SLUG if settings.DEBUG else self.region.slug
        try:
            async with session.post(
                settings.SUMM_AI_API_URL,
                headers={"Authorization": f"Bearer {settings.SUMM_AI_API_KEY}"},
                json={
                    "input_text": text_field.text,
                    "user": user,
                    "separator": settings.SUMM_AI_SEPARATOR,
                    "is_test": settings.SUMM_AI_TEST_MODE,
                    "is_initial": settings.SUMM_AI_IS_INITIAL,
                },
            ) as response:
                # Wait for the response
                response_data = await response.json()
                # Check whether the text was translated successfully
                if "translated_text" not in response_data:
                    if "error" in response_data:
                        raise SummAiException(
                            f"API error: {response.status} - {response_data['error']}"
                        )
                    raise SummAiException(
                        f"Unexpected API result: {response.status} - {response_data!r}"
                    )
                # Let the field handle the translated text
                text_field.translate(response_data["translated_text"])
                return text_field
        except (aiohttp.ClientError, asyncio.TimeoutError, SummAiException) as e:
            logger.error(
                "SUMM.AI translation of %r failed because of %s: %s",
                text_field,
                type(e),
                e,
            )
            text_field.exception = e
        return text_field

    async def translate_text_fields(
        self, loop: AbstractEventLoop, text_fields: Iterator[TextField]
    ) -> list[TextField]:
        """
        Translate a list of text fields from German into Easy German.
        Create an async task
        :meth:`~integreat_cms.summ_ai_api.summ_ai_api_client.SummAiApiClient.translate_text_field`
        for each entry.

        :param loop: The asyncio event loop
        :param text_fields: The text fields to be translated
        :returns: The list of completed text fields
        """
        # Set a custom SUMM.AI timeout
        timeout = aiohttp.ClientTimeout(total=60 * settings.SUMM_AI_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Create tasks for each text field
            tasks = [
                loop.create_task(self.translate_text_field(session, text_field))
                for text_field in text_fields
            ]
            # Wait for all tasks to finish and collect the results
            # (the results are sorted in the order the tasks were created)
            return await asyncio.gather(*tasks)

    def translate_queryset(self, queryset: list[Page], language_slug: str) -> None:
        """
        Translate a queryset of content objects from German into Easy German.

        To increase the speed of the translations, all operations are parallelized.

        :param queryset: The queryset which should be translated
        :param language_slug: The target language slug to translate into
        """
        # Make sure both languages exist
        self.request.region.get_language_or_404(settings.SUMM_AI_GERMAN_LANGUAGE_SLUG)
        easy_german = self.request.region.get_language_or_404(
            settings.SUMM_AI_EASY_GERMAN_LANGUAGE_SLUG
        )

        # Initialize translation helpers for each object instance
        translation_helpers = [
            TranslationHelper(self.request, self.form_class, object_instance)
            for object_instance in queryset
        ]

        # Aggregate all strings that need to be translated
        text_fields = chain(
            *[
                translation_helper.get_text_fields()
                for translation_helper in translation_helpers
            ]
        )

        # Initialize async event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Translate queryset asynchronously in parallel
        loop.run_until_complete(self.translate_text_fields(loop, text_fields))

        # Commit changes to the database
        for translation_helper in translation_helpers:
            translation_helper.commit(easy_german)
