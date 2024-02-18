"""Модуль spectacular extensions."""

from typing import Any

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class EndpointAuthenticationExtension(OpenApiAuthenticationExtension):
    """Схема endpoint auth."""

    target_class = "email_auth_remote.authentication.EndpointAuthentication"
    name = "EndpointAuthentication"
    match_subclasses = True

    def get_security_definition(self, auto_schema: AutoSchema) -> Any:
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix=self.target.keyword,
        )
