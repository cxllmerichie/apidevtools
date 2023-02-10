from contextlib import suppress
from typing import Any
from asyncpg import Record

from .schema import Schema


class Records:
    def __init__(self, records: list[Record], schema_t: type = None):
        item_t, item = (Schema, lambda record: schema_t(**dict(record))) if schema_t else (dict, lambda record: dict(record))
        self.__records: list[item_t] = [item(record) for record in records]

    def all(self) -> list[Record] | list[dict[str, Any]]:
        return self.__records

    def first(self) -> Record | dict[str, Any] | None:
        try:
            return self.__records[0]
        except IndexError:
            return None

    def last(self) -> Record | dict[str, Any] | None:
        try:
            return self.__records[-1]
        except IndexError:
            return None

    def limit(self, value: int) -> 'Records':
        with suppress(IndexError):
            self.__records = self.__records[:value]
        return self

    def offset(self, value: int) -> 'Records':
        with suppress(IndexError):
            self.__records = self.__records[value:]
        return self

    def order_by(self, column: str, direction: str = 'ASC') -> 'Records':
        with suppress(AttributeError):
            self.__records = sorted(self.__records, key=lambda d: d[column])
        self.__records = reversed(self.__records) if direction == 'DESC' else self.__records
        return self
