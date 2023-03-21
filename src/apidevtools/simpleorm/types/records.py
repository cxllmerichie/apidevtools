from typing import MutableMapping, Any
from contextlib import suppress as _suppress

from .schema import Schema, SchemaType


Record = dict[str, Any] | Schema | None


class Records:
    def __init__(self, records: list[MutableMapping], schema_t: SchemaType = dict[str, Any]):
        if schema_t.__name__ == 'dict':
            record_t, unwrap = dict[str, Any], lambda record: dict(record)
        else:
            record_t, unwrap = Schema, lambda record: schema_t(**dict(record)).from_db()
        self.records: list[record_t] = [unwrap(record) for record in records]

        self._iter = iter(records)
        self._aiter = iter(records)

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._aiter)
        except StopIteration:
            raise StopAsyncIteration

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

    def order_by(self, columns: str | list[str], direction: str = 'ASC') -> 'Records':
        def keys(record) -> tuple:
            if not isinstance(record, dict):
                record = dict(record)
            return tuple([record[column] for column in columns])
        self.records = sorted(
            self.records,
            key=columns if isinstance(columns, str) else keys,
            reverse=(direction.upper() == 'DESC')
        )
        return self
