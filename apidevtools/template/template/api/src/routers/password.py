from fastapi import APIRouter, Depends, HTTPException
from string_utils import shuffle
import string
import random

router = APIRouter(tags=['Password'])


@router.get('/generate/', name='Generate password', response_model=dict[str, str])
def _(length: int = 20, symset: str = None, uppercase: bool = True, lowercase: bool = True, digits: bool = True, special: bool = True):
    if symset:
        return dict(password=shuffle(''.join([random.choice(symset) for _ in range(length)])))

    symset = []
    if uppercase:
        symset.append(string.ascii_uppercase)
    if lowercase:
        symset.append(string.ascii_lowercase)
    if digits:
        symset.append(string.digits)
    if special:
        symset.append(string.punctuation)
    random.shuffle(symset)
    subset_size = length // len(symset)
    password = ''
    for i in range(len(symset) - 1):
        for i in range(subset_size):
            password += random.choice(symset[i])
    while len(password) != length:
        password += random.choice(symset[-1])
    password = shuffle(password)
    return dict(password=password)
