from contextlib import suppress as _suppress

from .schema import Schema
from .types import SchemaType, Record


class Records:
    def __init__(self, records: list['SQLRecord'], schema_t: SchemaType = dict):
        if schema_t is dict:
            item_t, item = dict, lambda record: dict(record)
        else:
            item_t, item = Schema, lambda record: schema_t(**dict(record)).from_db()
        self.records: list[item_t] = [item(record) for record in records]

    def all(self) -> list[Record]:
        return self.records

    def first(self) -> Record:
        try:
            return self.records[0]
        except IndexError:
            return None

    def last(self) -> Record:
        try:
            return self.records[-1]
        except IndexError:
            return None

    def limit(self, value: int) -> 'Records':
        with _suppress(IndexError):
            self.records = self.records[:value]
        return self

    def offset(self, value: int) -> 'Records':
        with _suppress(IndexError):
            self.records = self.records[value:]
        return self

    def order_by(self, columns: list[str], direction: str = 'ASC') -> 'Records':
        def keys(record) -> tuple:
            if isinstance(record, dict):
                return tuple([record[column] for column in columns])
            return tuple([dict(record)[column] for column in columns])
        self.records = sorted(self.records, key=keys)
        if direction == 'DESC':
            self.records.reverse()
        return self
