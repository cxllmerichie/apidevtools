from typing import Any
import ast as _ast
import datetime


INF: int = 2147483647
LIMIT: int = 100


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow()


def evaluate(value: bytes, convert: bool = True) -> Any:
    """
    normal ast.literal_eval with a fix of known error together wit adaptation to the apidevtools package
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


def is_dict(subscripted_dict_type: type[dict]) -> bool:
    """
    compares `dict[Any, Any]` with `dict`, normally done using `is`, but does not work for typehinted types
    :param subscripted_dict_type:
    :return:
    """
    return subscripted_dict_type.__name__ == 'dict'
