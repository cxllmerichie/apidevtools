import datetime as _datetime
from dateutil.parser import parse as _parse


def utcnow() -> _datetime.datetime:
    return _datetime.datetime.utcnow()


def str_to_dt(str_dt: str) -> _datetime.datetime:
    return _parse(str_dt)
