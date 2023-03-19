from pydantic import BaseModel
from abc import ABC
from abc import abstractmethod as _abstractmethod
from contextlib import suppress as _suppress
from typing import MutableMapping, Any
import datetime


class Relation:
    def __init__(self, tablename: str, where: dict[str, Any], ext_schema_t: 'SchemaType', fieldname: str,
                 rel_schema_t: 'SchemaType' = dict, columns: list[str] = None):
        self.tablename: str = tablename
        self.where: dict[str, Any] = where
        self.ext_schema_t: SchemaType = ext_schema_t
        self.fieldname: str = fieldname
        self.rel_schema_t: SchemaType = rel_schema_t
        self.columns: list[str] = columns if columns else ['*']


class Schema(BaseModel, ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        """
        Abstract property, supposed to handles name of the database table
        :return:
        """
        ...

    def relations(self) -> list[Relation]:
        return []

    def serializable(self, types: tuple[type, ...] = (datetime.datetime, datetime.date, datetime.time)) -> dict[str: Any]:
        """
        Returns python dictionary of values which will not trigger FastAPI error related to not serializable objects
        :param types:
        :return:
        """
        return {key: str(value) if isinstance(value, types) else value for key, value in dict(self).items()}

    def into_db(self) -> 'Schema':
        return self

    def from_db(self) -> 'Schema':
        return self


Instance = dict[str, Any] | Schema
SchemaType = type[dict[str, Any] | Schema]
Record = dict[str, Any] | Schema | None


class Records:
    def __init__(self, records: list[MutableMapping], schema_t: SchemaType = dict[str, Any]):
        if schema_t.__name__ == 'dict':
            record_t, unwrap = dict[str, Any], lambda record: dict(record)
        else:
            record_t, unwrap = Schema, lambda record: schema_t(**dict(record)).from_db()
        self.records: list[record_t] = [unwrap(record) for record in records]

    # implement a few more methods but keep existing
    # `for . in Records`
    # `async for . in Records`
    # `Records[0] and len(Records)`

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
