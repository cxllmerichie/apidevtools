from cryptography.hazmat.primitives.ciphers.aead import AESGCM as _AESGCM
import ast as _ast
import secrets as _secrets
from typing import Any


def randkey() -> bytes:
    return _secrets.token_bytes(32)


def encrypt(data: Any, key: bytes = randkey(), associated_data: bytes | str | None = None)\
        -> tuple[bytes, bytes]:
    nonce = _secrets.token_bytes(12)
    if associated_data:
        associated_data = associated_data if isinstance(associated_data, bytes) else associated_data.encode()
    return nonce + _AESGCM(key).encrypt(nonce, str(data).encode(), associated_data), key


def decrypt(data: bytes, key: bytes, associated_data: bytes | str | None = None, *, convert: bool = False)\
        -> Any:
    if associated_data:
        associated_data = associated_data if isinstance(associated_data, bytes) else associated_data.encode()
    decrypted = _AESGCM(key).decrypt(data[:12], data[12:], associated_data)
    if not convert:
        return decrypted
    try:
        return _ast.literal_eval(decrypted.decode())
    except ValueError:
        return _ast.literal_eval(f'\'{decrypted.decode()}\'')
    except SyntaxError:
        return decrypted.decode()
