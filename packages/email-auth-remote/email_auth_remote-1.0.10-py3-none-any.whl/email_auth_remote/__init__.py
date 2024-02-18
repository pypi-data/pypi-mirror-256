"""
Инициализирует пакет
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("email-auth-remote")
except PackageNotFoundError:
    # package is not installed
    __version__ = None
