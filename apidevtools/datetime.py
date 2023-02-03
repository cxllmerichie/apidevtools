from datetime import datetime
from dateutil.parser import parse


def utcnow() -> datetime:
    return datetime.utcnow()


def str_to_dt(dt: str) -> datetime:
    return parse(dt)
