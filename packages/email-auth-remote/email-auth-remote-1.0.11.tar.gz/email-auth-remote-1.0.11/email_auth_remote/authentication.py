"""Модуль аутентификации с помощью auth endpoint."""

import logging
from typing import Optional, Tuple
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework.request import Request
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import requests
from .models import RemoteEmailUser

logger = logging.getLogger(__name__)


class EndpointAuthentication(BaseAuthentication):
    """
    Аутентификация с помощью auth endpoint (settings.AUTH_ENDPOINT_URL).
    В случае успеха заменяет модель пользователя у request на RemoteEmailUser.
    """

    www_authenticate_realm = "api"
    media_type = "application/json"
    keyword = "Bearer"

    def authenticate_header(self, request: Request) -> str:
        return f'{self.keyword} realm="{self.www_authenticate_realm}"'

    def authenticate(self, request: Request) -> Optional[Tuple[RemoteEmailUser, None]]:
        auth = get_authorization_header(request)

        if not auth:
            return None

        try:
            response = requests.get(
                settings.AUTH_ENDPOINT_URL,  # type: ignore[misc]
                timeout=10,
                headers={"Authorization": auth},
            )
            response.raise_for_status()
            user_data = response.json()
            user = RemoteEmailUser(user_id=user_data["id"], email=user_data["email"])
            return user, None
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
        ) as error:
            logger.error(str(error))
            raise exceptions.APIException(
                detail=_("Could not connect to authentication server.")
            )
        except requests.exceptions.HTTPError as http_err:
            raise exceptions.AuthenticationFailed(detail=http_err.response.json())
        except KeyError as exc:
            raise exceptions.APIException(
                detail=_(
                    "Invalid user credentials. Maybe authentication api has changed?"
                )
            ) from exc
        except Exception as exc:
            logger.exception(str(exc))
            raise exceptions.APIException(
                detail=_("Something went wrong. Please try again.")
            )
