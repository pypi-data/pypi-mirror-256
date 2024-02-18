from importlib.metadata import PackageNotFoundError, version

print("loaded")

try:
    __version__ = version("email-auth-remote")
except PackageNotFoundError:
    # package is not installed
    __version__ = None

print(__version__)
