from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher._mode_cfb import CfbMode


__iv = Random.new().read(AES.block_size)


def __cipher(key: bytes) -> CfbMode:
    return AES.new(key, AES.MODE_CFB, __iv)


def encrypt(data: str, key: bytes) -> str:
    data_bytes = data.encode()
    encrypted_bytes = __iv + __cipher(key).encrypt(data_bytes)
    return encrypted_bytes.hex()


def decrypt(encrypted: str, key: bytes) -> str:
    encrypted_bytes = bytes.fromhex(encrypted)
    decrypted_bytes = __cipher(key).decrypt(encrypted_bytes)[len(__iv):]
    return decrypted_bytes.decode()


def key(str_key: str) -> bytes:
    return str_key.encode()
