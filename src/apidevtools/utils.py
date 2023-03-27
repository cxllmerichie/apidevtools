from typing import Any
import ast as _ast


INF: int = 2147483647
LIMIT: int = 100


def evaluate(value: bytes, convert: bool = True) -> Any:
    if not convert:
        return value
    try:
        return _ast.literal_eval(value.decode())
    except ValueError:
        return _ast.literal_eval(f'\'{value.decode()}\'')
    except SyntaxError:
        return value.decode()
