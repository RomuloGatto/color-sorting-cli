import warnings
from typing import Any, Callable


def deprecate(new_function: Callable[..., Any]):
    """Trigger a warning of deprecated function and calls the new function instead

    Args:
        new_function (Callable[..., Any]): new function
    """

    def deprecated_function(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            f"Please use '{new_function.__name__}' instead.",
            DeprecationWarning,
            2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        return new_function(*args, **kwargs)

    return deprecated_function
