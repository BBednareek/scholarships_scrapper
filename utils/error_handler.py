import asyncio
import functools
from typing import Callable, Any


class DataFetchError(Exception):
    """Raised when an error occurs during data fetching."""


class DataConversionError(Exception):
    """Raised when an error occurs during data parsing/conversion."""


class DataSendError(Exception):
    """Raised when an error occurs during sending data to external systems."""


def error_handler(stage: str) -> Callable:
    """
    Universal decorator for handling errors in different data processing stages.

    Args:
        stage (str): Must be one of 'fetch', 'convert', 'send'.

    Returns:
        Callable: Wrapped function with stage-specific error handling.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise _raise_stage_error(stage, func.__name__, e)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise _raise_stage_error(stage, func.__name__, e)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


def _raise_stage_error(stage: str, func_name: str, error: Exception) -> None:
    message: str = f"[{stage.upper()} ERROR] {func_name}: {error}"
    if stage == "fetch":
        raise DataFetchError(message)
    elif stage == "convert":
        raise DataConversionError(message)
    elif stage == "send":
        raise DataSendError(message)
    else:
        raise RuntimeError(f"[UNKNOWN STAGE] {func_name}: {error}")
