import Crypto as _Crypto
from typing import Any
import ast as _ast
import string as _string
import random as _random


KeyType = bytes | str


def randiv() -> bytes:
    return _Crypto.Cipher.Random.new().read(_Crypto.Cipher.AES.block_size)


def randkey(key_t: type[bytes | str] = str) -> KeyType:
    length, symset = 16, [_string.ascii_uppercase, _string.ascii_lowercase, _string.digits, _string.punctuation]
    _random.shuffle(symset)
    password = ''
    for i in range(len(symset) - 1):
        for _ in range(length // len(symset)):
            password += _random.choice(symset[i])
    while len(password) != length:
        password += _random.choice(symset[-1])
    password = ''.join(_random.sample(password, len(password)))
    return password if key_t is str else password.encode()


def __cipher(key: KeyType, iv: bytes) -> _Crypto.Cipher._mode_cfb.CfbMode:
    key = key.encode() if isinstance(key, str) else key
    return _Crypto.Cipher.AES.new(key, _Crypto.Cipher.AES.MODE_CFB, iv)


def encrypt(to_encrypt: Any, key: KeyType, iv: bytes = randiv()) -> tuple[bytes, bytes]:
    to_encrypt_bytes = str(to_encrypt).encode()
    encrypted_bytes = iv + __cipher(key, iv).encrypt(to_encrypt_bytes)
    return encrypted_bytes, iv


def decrypt(encrypted: bytes | str, key: KeyType, iv: bytes, convert: bool = False) -> bytes | Any:
    encrypted_bytes = encrypted if isinstance(encrypted, bytes) else encrypted.decode()
    decrypted_bytes = __cipher(key, iv).decrypt(encrypted_bytes)[len(iv):]
    return decrypted_bytes if not convert else _ast.literal_eval(decrypted_bytes.decode())

