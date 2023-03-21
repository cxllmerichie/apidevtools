from typing import MutableMapping, Any
from contextlib import suppress as _suppress

from .schema import Schema, SchemaType


Record = dict[str, Any] | Schema | None


class Records:
    def __init__(self, records: list[MutableMapping], schema_t: SchemaType = dict[str, Any]):
        if schema_t.__name__ == 'dict':
            self.record_t, self.unwrap = dict[str, Any], lambda record: dict(record)
        elif schema_t.__class__.__name__ == 'ModelMetaclass':
            self.record_t, self.unwrap = Schema, lambda record: schema_t(**dict(record)).from_db()
        self._records: list = [self.unwrap(record) for record in records]

        self._iter = iter(records)
        self._aiter = iter(records)

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iter)

    def __aiter__(self):
        return self

    def __setitem__(self, index: int, value):
        self._records[index] = value

    async def __anext__(self):
        try:
            return next(self._aiter)
        except StopIteration:
            raise StopAsyncIteration

    def all(self) -> list[Record]:
        return self._records

    def first(self) -> Record:
        try:
            return self._records[0]
        except IndexError:
            return None

    def last(self) -> Record:
        try:
            return self._records[-1]
        except IndexError:
            return None

    def limit(self, length: int) -> 'Records':
        with _suppress(IndexError):
            self._records = self._records[:length]
        return self

    def offset(self, length: int) -> 'Records':
        with _suppress(IndexError):
            self._records = self._records[length:]
        return self

    def order_by(self, columns: str | list[str], direction: str = 'ASC') -> 'Records':
        def keys(record) -> tuple:
            if not isinstance(record, dict):
                record = dict(record)
            return tuple([record[column] for column in columns])
        self._records = sorted(
            self._records,
            key=columns if isinstance(columns, str) else keys,
            reverse=(direction.upper() == 'DESC')
        )
        return self
