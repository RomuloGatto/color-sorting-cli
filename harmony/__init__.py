from importlib.metadata import PackageNotFoundError, version

__app_name__ = "Harmony"

try:
    __version__ = version(__app_name__)

except PackageNotFoundError:
    __version__ = "1.0.0"
