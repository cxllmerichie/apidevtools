from contextlib import suppress
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


class Hasher:
    error: Exception = VerifyMismatchError
    hasher: PasswordHasher = PasswordHasher()

    def hash(self, password: str) -> str:
        """
        Overwrite the method, if prefer another algorithm not changing the func name.
        Purpose: creates hash of password.
        :param password: plain password string
        :return: hashed password string
        """
        return self.hasher.hash(password=password)

    def cmp(self, pw_hash: str, password: str) -> bool:
        """
        Overwrite the method, if prefer another algorithm not changing the func name.
        Purpose: compares hash and password.
        :param pw_hash: hashed password string
        :param password: plain password string
        :return: True if password matches, False otherwise
        """
        with suppress(self.error, VerificationError, InvalidHash):
            return self.hasher.verify(hash=pw_hash, password=password) is True


HASHER = Hasher()
