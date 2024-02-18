from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import URLValidator

if not hasattr(settings, "AUTH_ENDPOINT_URL"):
    raise ImproperlyConfigured("AUTH_ENDPOINT_URL must be set in settings.")

try:
    URLValidator()(settings.AUTH_ENDPOINT_URL)  # type: ignore[misc]
except ValidationError as exc:
    raise ImproperlyConfigured("AUTH_ENDPOINT_URL must be a valid URL.") from exc

AUTH_ENDPOINT_URL = getattr(settings, "AUTH_ENDPOINT_URL")
