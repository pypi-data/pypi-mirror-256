"""Модуль моделей для email_auth_remote."""

from functools import cached_property
from typing import Optional, List
from django.db.models.manager import EmptyManager
from django.contrib.auth import models as auth_models


class RemoteEmailUser:
    """
    Класс пользователя для email_auth_remote.EndpointAuthentication.

    Пользователя нельзя сохранить в БД.
    """

    _is_staff = False
    _is_active = True
    _is_superuser = False

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, user_id: int, email: str) -> None:
        self._id = user_id
        self._email = email

    def __str__(self) -> str:
        return f"RemoteEmailUser {self.id}"

    @cached_property
    def id(self) -> int:
        """ID пользователя."""
        return self._id

    @cached_property
    def pk(self) -> int:
        """Primary Key пользователя. В данном случае = ID."""
        return self.id

    @cached_property
    def email(self) -> str:
        """Email пользователя."""
        return self._email

    @cached_property
    def is_staff(self) -> bool:
        """
        Пользователь не staff.
        Не уверен, что доступ к админке можно получить с таким пользователем
        (пользователь для админки должен быть сохранен в БД).
        """
        return self._is_staff

    @cached_property
    def is_superuser(self) -> bool:
        """
        Пользователь не superuser.
        Не уверен, что доступ к админке можно получить с таким пользователем
        (пользователь для админки должен быть сохранен в БД).
        """
        return self._is_superuser

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RemoteEmailUser):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def save(self) -> None:
        """Пользователя нельзя сохранить в БД."""
        raise NotImplementedError("Remote email users have no DB representation")

    def delete(self) -> None:
        """Пользователя нельзя сохранить в БД."""
        raise NotImplementedError("Remote email users have no DB representation")

    def set_password(self, raw_password: str) -> None:
        """Пользователя нельзя сохранить в БД."""
        raise NotImplementedError("Remote email users have no DB representation")

    def check_password(self, raw_password: str) -> None:
        """Пользователя нельзя сохранить в БД."""
        raise NotImplementedError("Remote email users have no DB representation")

    @property
    def groups(self) -> auth_models.Group:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permission are not implemented yet.")
        # return self._groups

    @property
    def user_permissions(self) -> auth_models.Permission:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")
        # return self._user_permissions

    def get_group_permissions(self, obj: Optional[object] = None) -> set:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")

    def get_all_permissions(self, obj: Optional[object] = None) -> set:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")

    def has_perms(self, perm_list: List[str], obj: Optional[object] = None) -> bool:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")

    def has_module_perms(self, module: str) -> bool:
        """У пользователя нет Group и Permissions. WIP."""
        raise NotImplementedError("Remote auth permissions are not implemented yet.")

    @property
    def is_anonymous(self) -> bool:
        """Пользователь не анонимный."""
        return False

    @property
    def is_authenticated(self) -> bool:
        """Пользователь всегда аутентифицирован."""
        return True

    def get_username(self) -> str:
        """У пользователя email вместо имени."""
        return self._email
