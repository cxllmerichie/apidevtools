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

    def limit(self, value: int) -> list[Record] | list[dict[str, Any]]:
        try:
            return self.__records[:value]
        except IndexError:
            return self.all()

    def offset(self, value: int) -> list[Record] | list[dict[str, Any]]:
        try:
            return self.__records[value:]
        except IndexError:
            return self.all()
