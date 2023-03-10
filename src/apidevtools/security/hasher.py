from contextlib import suppress as _suppress
from argon2 import PasswordHasher as _PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


error: type[Exception] = VerifyMismatchError
__hasher: _PasswordHasher = _PasswordHasher()


def hash(password: str) -> str:
    """

    :param password: plain password string
    :return: hashed password string
    """
    return __hasher.hash(password=password)


def cmp(pw_hash: str, password: str) -> bool:
    """

    :param pw_hash: hashed password string
    :param password: plain password string
    :return: True if password matches, False otherwise
    """
    with _suppress(VerifyMismatchError, VerificationError, InvalidHash):
        return __hasher.verify(hash=pw_hash, password=password) is True
