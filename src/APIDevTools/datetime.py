from datetime import datetime
from dateutil.parser import parse


def utcnow() -> datetime:
    return datetime.utcnow()


def str_to_dt(str_dt: str) -> datetime:
    return parse(str_dt)
