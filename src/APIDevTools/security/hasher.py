from contextlib import suppress
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


error: Exception = VerifyMismatchError
hasher: PasswordHasher = PasswordHasher()


def hash(password: str) -> str:
    """
    Overwrite the method, if prefer another algorithm not changing the func name.
    Purpose: creates hash of password.
    :param password: plain password string
    :return: hashed password string
    """
    return hasher.hash(password=password)


def cmp(pw_hash: str, password: str) -> bool:
    """
    Overwrite the method, if prefer another algorithm not changing the func name.
    Purpose: compares hash and password.
    :param pw_hash: hashed password string
    :param password: plain password string
    :return: True if password matches, False otherwise
    """
    with suppress(VerifyMismatchError, VerificationError, InvalidHash):
        return hasher.verify(hash=pw_hash, password=password) is True
