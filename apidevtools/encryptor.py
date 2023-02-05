from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher._mode_cfb import CfbMode


class Encryptor:
    __iv = Random.new().read(AES.block_size)

    @staticmethod
    def __cipher(key: bytes) -> CfbMode:
        return AES.new(key, AES.MODE_CFB, Encryptor.__iv)

    @staticmethod
    def encrypt(data: str, key: bytes) -> str:
        data_bytes = data.encode()
        encrypted_bytes = Encryptor.__iv + Encryptor.__cipher(key).encrypt(data_bytes)
        return encrypted_bytes.hex()

    @staticmethod
    def decrypt(encrypted: str, key: bytes) -> str:
        encrypted_bytes = bytes.fromhex(encrypted)
        decrypted_bytes = Encryptor.__cipher(key).decrypt(encrypted_bytes)[len(Encryptor.__iv):]
        return decrypted_bytes.decode()

    @staticmethod
    def key(str_key: str) -> bytes:
        return str_key.encode()
