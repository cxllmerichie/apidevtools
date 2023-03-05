from contextlib import suppress as _suppress
from typing import MutableMapping, Any

from .types import SchemaType, Record
from .schema import Schema


class Records:
    def __init__(self, records: list[MutableMapping], schema_t: SchemaType = dict[str, Any]):
        # if schema_t is dict[str, Any]: returns False if "schema_t" has default value "dict[str, Any]"
        # to fix: find out how to compare advanced typehinted types, like dict[str, Any]
        if str(schema_t) == str(dict[str, Any]):
            record_t, unwrap = dict[str, Any], lambda record: dict(record)
        else:
            record_t, unwrap = Schema, lambda record: schema_t(**dict(record)).from_db()
        self.records: list[record_t] = [unwrap(record) for record in records]

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

    def limit(self, length: int) -> 'Records':
        with _suppress(IndexError):
            self.records = self.records[:length]
        return self

    def offset(self, length: int) -> 'Records':
        with _suppress(IndexError):
            self.records = self.records[length:]
        return self

    def order_by(self, columns: list[str], direction: str = 'ASC') -> 'Records':
        def keys(record) -> tuple:
            if not isinstance(record, dict):
                record = dict(record)
            return tuple([record[column] for column in columns])
        self.records = sorted(self.records, key=keys, reverse=(direction == 'DESC'))
        return self
