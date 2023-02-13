from Crypto.Cipher import AES as _AES
from Crypto import Random as _Random
from Crypto.Cipher._mode_cfb import CfbMode as _CfbMode


__iv = _Random.new().read(_AES.block_size)


def __cipher(key: bytes) -> _CfbMode:
    return _AES.new(key, _AES.MODE_CFB, __iv)


def encrypt(data: str, key: bytes) -> str:
    data_bytes = data.encode()
    encrypted_bytes = __iv + __cipher(key).encrypt(data_bytes)
    return encrypted_bytes.hex()


def decrypt(encrypted: str, key: bytes) -> str:
    encrypted_bytes = bytes.fromhex(encrypted)
    decrypted_bytes = __cipher(key).decrypt(encrypted_bytes)[len(__iv):]
    return decrypted_bytes.decode()


def key(str_key: str) -> bytes:
    if len(str_key) != 16:
        raise AssertionError('Encryption key length must be 16 characters.')
    return str_key.encode()
