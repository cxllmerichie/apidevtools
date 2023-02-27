from Crypto.Cipher import AES as _AES
from Crypto import Random as _Random
from Crypto.Cipher._mode_cfb import CfbMode as _CfbMode
from typing import Any
import ast as _ast


KeyType = bytes | str


def __cipher(key: KeyType, iv: bytes) -> _CfbMode:
    key = key.encode() if isinstance(key, str) else key
    return _AES.new(key, _AES.MODE_CFB, iv)


def randiv() -> bytes:
    return _Random.new().read(_AES.block_size)


def encrypt(to_encrypt: Any, key: KeyType, iv: bytes = randiv()) -> tuple[bytes, bytes]:
    to_encrypt_bytes = str(to_encrypt).encode()
    encrypted_bytes = iv + __cipher(key, iv).encrypt(to_encrypt_bytes)
    return encrypted_bytes, iv


def decrypt(encrypted: bytes | str, key: KeyType, iv: bytes, convert: bool = False) -> bytes | Any:
    encrypted_bytes = encrypted if isinstance(encrypted, bytes) else encrypted.decode()
    decrypted_bytes = __cipher(key, iv).decrypt(encrypted_bytes)[len(iv):]
    return decrypted_bytes if not convert else _ast.literal_eval(decrypted_bytes.decode())
