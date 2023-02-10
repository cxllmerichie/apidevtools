from contextlib import suppress
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from abc import ABC


class Hasher(ABC):
    error: Exception = VerifyMismatchError
    hasher: PasswordHasher = PasswordHasher()

    @staticmethod
    def hash(password: str) -> str:
        """
        Overwrite the method, if prefer another algorithm not changing the func name.
        Purpose: creates hash of password.
        :param password: plain password string
        :return: hashed password string
        """
        return Hasher.hasher.hash(password=password)

    @staticmethod
    def cmp(pw_hash: str, password: str) -> bool:
        """
        Overwrite the method, if prefer another algorithm not changing the func name.
        Purpose: compares hash and password.
        :param pw_hash: hashed password string
        :param password: plain password string
        :return: True if password matches, False otherwise
        """
        with suppress(VerifyMismatchError, VerificationError, InvalidHash):
            return Hasher.hasher.verify(hash=pw_hash, password=password) is True
