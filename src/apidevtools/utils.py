from typing import Any
import ast as _ast


INF: int = 2147483647
LIMIT: int = 100


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


def is_dict(typehinted: type) -> bool:
    """
    compares `dict[Any, Any]` with `dict`, normally done using `is`, but does not work for typehinted types
    :param typehinted:
    :return:
    """
    return typehinted.__name__ == 'dict'
