from typing import Awaitable, Any, Callable
from functools import cache, wraps as _wraps
import ast as _ast
import datetime


INF: int = 2147483647
LIMIT: int = 100


class _CachedAwaitable:
    """
    Allows to make a coroutine reawaitable.
    """
    _ResultUnset: str = 'CachedAwaitableResultUnset'

    def __init__(self, awaitable: Awaitable):
        self.awaitable: Awaitable = awaitable
        self.result: Any = _CachedAwaitable._ResultUnset

    def __await__(self) -> Any:
        if self.result == _CachedAwaitable._ResultUnset:
            self.result = yield from self.awaitable.__await__()
        return self.result


def reawaitable(func: Callable, /):
    """
    Makes a coroutine reawaitable.
    :param func:
    :return:
    """
    @_wraps(func)
    def wrapper(*args, **kwargs):
        return _CachedAwaitable(func(*args, **kwargs))
    return wrapper


def aiocache(func: Callable, /):
    """
    `functools.cache` for coroutines.
    :param func:
    :return:
    """
    return cache(reawaitable(func))


def now_tz_aware() -> datetime.datetime:
    """
    `datetime.now()` with timezone info.
    :return:
    """
    return datetime.datetime.now(datetime.timezone.utc)


def now_tz_naive() -> datetime.datetime:
    """
    `datetime.now()` without timezone info.
    :return:
    """
    dt = datetime.datetime.now()
    dt.replace(tzinfo=None)
    return dt


def evaluate(value: bytes, convert: bool = True) -> Any:
    """
    Normal `ast.literal_eval` with a fix of known error together wit adaptation to the apidevtools package.
    :param value:
    :param convert:
    :return:
    """
    if not convert:
        return value
    try:
        return _ast.literal_eval(value.decode())
    except ValueError:
        return _ast.literal_eval(f'\'{value.decode()}\'')
    except SyntaxError:
        return value.decode()
    except AttributeError:
        return None


def is_dict(type: type[dict[Any, Any]], /) -> bool:
    """
    Compares `dict[Any, Any]` with `dict`, normally done using `is`, but does not work for subscripted types.
    :param type:
    :return: True if `dict` type passed, otherwise False.
    """
    return type.__name__ == 'dict'
