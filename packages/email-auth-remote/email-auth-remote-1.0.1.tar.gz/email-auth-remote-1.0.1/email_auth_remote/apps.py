"""Конфигурация email_auth_remote"""

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator


class EmailAuthRemoteConfig(AppConfig):
    """
    Конфигурация email_auth_remote.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "email_auth_remote"

    def ready(self) -> None:
        if not hasattr(settings, "AUTH_ENDPOINT_URL"):
            raise ImproperlyConfigured("AUTH_ENDPOINT_URL must be set in settings.")

        try:
            URLValidator()(settings.AUTH_ENDPOINT_URL)  # type: ignore[misc]
        except ValidationError as exc:
            raise ImproperlyConfigured(
                "AUTH_ENDPOINT_URL must be a valid URL."
            ) from exc
