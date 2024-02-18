"""
This module contains the base view for bulk actions
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cacheops import invalidate_model
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic.list import MultipleObjectMixin

from ..constants import status
from ..models import Page
from .utils.stringify_list import iter_to_string
from .utils.translation_status import change_translation_status

if TYPE_CHECKING:
    from typing import Any

    from django.forms import ModelForm
    from django.http import HttpRequest, HttpResponse
    from django.http.response import HttpResponseRedirect

logger = logging.getLogger(__name__)


class BulkActionView(PermissionRequiredMixin, MultipleObjectMixin, RedirectView):
    """
    View for executing a bulk action and redirect to a given location
    """

    #: The list of HTTP method names that this view will accept.
    #: The bulk action form uses only POST as submission method.
    http_method_names: list[str] = ["post"]
    #: Whether the view requires change permissions
    require_change_permission: bool = True
    #: Whether the translation objects should be prefetched
    prefetch_translations: bool = False
    #: Whether the public translation objects should be prefetched
    prefetch_public_translations: bool = False

    def get_permission_required(self) -> tuple[str]:
        """
        Override this method to override the permission_required attribute.

        :return: The permissions that are required for views inheriting from this Mixin
        """
        # If the bulk action performs changes to the database, require the change permission
        if self.require_change_permission:
            return (f"cms.change_{self.model._meta.model_name}",)
        # If the bulk action is just a read-view (e.g. export), require the view permission
        return (f"cms.view_{self.model._meta.model_name}",)

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        r"""
        Retrieve url for redirection

        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: url to redirect to
        """
        redirect_kwargs = {
            "region_slug": self.request.region.slug,
        }
        # If this bulk action is bound to a language url parameter, also pass this to the redirect url
        if "language_slug" in kwargs:
            redirect_kwargs["language_slug"] = kwargs["language_slug"]
        return reverse(f"{self.model._meta.model_name}s", kwargs=redirect_kwargs)

    def get_queryset(self) -> Any:
        """
        Get the queryset of selected items for this bulk action

        :raises ~django.http.Http404: HTTP status 404 if no objects with the given ids exist

        :return: The QuerySet of the filtered links
        """
        # This workaround is necessary to enable the async tests for the SUMM.AI client
        logger.debug("request body: %s", self.request.body)
        queryset = (
            super()
            .get_queryset()
            .filter(
                region=self.request.region,
                id__in=self.request.POST.getlist("selected_ids[]"),
            )
        )
        if not queryset:
            raise Http404(f"No {self.model._meta.object_name} matches the given query.")
        if self.prefetch_translations:
            queryset = queryset.prefetch_translations()
        if self.prefetch_public_translations:
            queryset = queryset.prefetch_public_translations()
        return queryset


class BulkMachineTranslationView(BulkActionView):
    """
    Bulk action for automatically translating multiple objects
    """

    #: Whether the public translation objects should be prefetched
    prefetch_translations: bool = True

    #: the form of this bulk action
    form: ModelForm | None = None

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        r"""
        Translate multiple objects automatically

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """
        if TYPE_CHECKING:
            assert self.form
        language_slug = kwargs["language_slug"]
        language_node = request.region.language_node_by_slug.get(language_slug)
        if not language_node or not language_node.active:
            raise Http404("No language matches the given query.")
        if not language_node.mt_provider:
            messages.error(
                request,
                _('Machine translations are disabled for language "{}"').format(
                    language_node
                ),
            )
            return super().post(request, *args, **kwargs)
        if not language_node.mt_provider.is_permitted(
            request.region, request.user, self.form._meta.model
        ):
            messages.error(
                request,
                _(
                    "Machine translations are not allowed for the current user or content type"
                ).format(language_node),
            )
            return super().post(request, *args, **kwargs)
        if language_node.mt_provider.bulk_only_for_staff and not request.user.is_staff:
            raise PermissionDenied(
                f"Only staff users have the permission to bulk translate {self.form._meta.model._meta.model_name} via {language_node.mt_provider}"
            )

        to_translate = language_node.mt_provider.is_needed(
            request.region, self.get_queryset(), language_node
        )
        if not to_translate:
            messages.error(
                request,
                _("All the selected translations are already up-to-date."),
            )
            return super().post(request, *args, **kwargs)

        for content_object in self.get_queryset():
            if not content_object in to_translate:
                messages.error(
                    request,
                    _("There already is an up-to-date translation for {}").format(
                        content_object.best_translation.title,
                    ),
                )

        logger.debug(
            "Machine translation via %s into %r for: %r",
            language_node.mt_provider.name,
            language_node.language,
            to_translate,
        )
        api_client = language_node.mt_provider.api_client(request, self.form)
        api_client.translate_queryset(to_translate, language_node.slug)

        # Let the base view handle the redirect
        return super().post(request, *args, **kwargs)


class BulkUpdateBooleanFieldView(BulkActionView):
    """
    Bulk action for toggling boolean fields of multiple objects at once
    """

    #: The value of the field (defaults to ``True``)
    value: bool = True

    @property
    def field_name(self) -> str:
        """
        Called when the bulk action is performed and the ``field_name`` attribute was not overwritten

        :raises NotImplementedError: If the ``field_name`` attribute is not implemented in the subclass
        """
        raise NotImplementedError(
            "Subclasses of BulkUpdateBooleanFieldView must provide a 'field_name' attribute"
        )

    @property
    def action(self) -> str:
        """
        Called when the bulk action is performed and the ``action`` attribute was not overwritten

        :raises NotImplementedError: If the ``action`` attribute is not implemented in the subclass
        """
        raise NotImplementedError(
            "Subclasses of BulkUpdateBooleanFieldView must provide an 'action' attribute"
        )

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        r"""
        Update the fields of the selected objects and redirect

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """

        # Archive objects
        self.get_queryset().update(**{self.field_name: self.value})
        # Invalidate cache
        invalidate_model(self.model)
        logger.debug(
            "Updated %s=%s for %r by %r",
            self.field_name,
            self.value,
            self.get_queryset(),
            request.user,
        )
        messages.success(
            request,
            _("The selected {} were successfully {}").format(
                self.model._meta.verbose_name_plural, self.action
            ),
        )
        # Let the base view handle the redirect
        return super().post(request, *args, **kwargs)


class BulkArchiveView(BulkActionView):
    """
    Bulk action for restoring multiple objects at once
    """

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        r"""
        Archive multiple objects

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """
        if self.model is Page:
            for content_object in self.get_queryset():
                if content_object.mirroring_pages.exists():
                    messages.error(
                        request,
                        _(
                            'Page "{}" cannot be archived because it was embedded as live content from another page.'
                        ).format(content_object.best_translation),
                    )
                else:
                    messages.success(
                        request,
                        _('Page "{}" was successfully archived').format(
                            content_object.best_translation
                        ),
                    )
                    content_object.archive()
        else:
            for content_object in self.get_queryset():
                content_object.archive()
            messages.success(
                request,
                _("The selected {} were successfully archived").format(
                    self.model._meta.verbose_name_plural
                ),
            )

        # Invalidate cache
        invalidate_model(self.model)
        logger.debug(
            "archived %r by %r",
            self.get_queryset(),
            request.user,
        )
        return super().post(request, *args, **kwargs)


class BulkRestoreView(BulkActionView):
    """
    Bulk action for restoring multiple objects at once
    """

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:
        r"""
        Restore multiple objects

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """
        restore_failed = []
        for content_object in self.get_queryset():
            if self.get_queryset().model is Page and content_object.implicitly_archived:
                restore_failed.append(content_object)
            else:
                content_object.restore()

        if restore_failed:
            messages.error(
                request,
                _(
                    "The following {} could not be restored because they have at least one archived parent {}: {}"
                ).format(
                    self.model._meta.verbose_name_plural,
                    self.model._meta.verbose_name,
                    iter_to_string(
                        [object.best_translation.title for object in restore_failed]
                    ),
                ),
            )

        restore_succeeded = self.get_queryset().exclude(
            id__in=[page.id for page in restore_failed]
        )

        if restore_succeeded:
            messages.success(
                request,
                _("The following {} were successfully restored: {}").format(
                    self.model._meta.verbose_name_plural,
                    iter_to_string(
                        [object.best_translation.title for object in restore_succeeded]
                    ),
                ),
            )

        # Invalidate cache
        invalidate_model(self.model)

        return super().post(request, *args, **kwargs)


class BulkPublishingView(BulkActionView):
    """
    Bulk action to publish multiple pages at once
    """

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        r"""
        Function to change the translation status to publish of multiple pages at once

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """
        change_translation_status(
            request, self.get_queryset(), kwargs["language_slug"], status.PUBLIC
        )
        return super().post(request, *args, **kwargs)


class BulkDraftingView(BulkActionView):
    """
    Bulk action to draft multiple pages at once
    """

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        r"""
        Function to change the translation status to draft of multiple pages at once

        :param request: The current request
        :param \*args: The supplied arguments
        :param \**kwargs: The supplied keyword arguments
        :return: The redirect
        """
        change_translation_status(
            request, self.get_queryset(), kwargs["language_slug"], status.DRAFT
        )
        return super().post(request, *args, **kwargs)
