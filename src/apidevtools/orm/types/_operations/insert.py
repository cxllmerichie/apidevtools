from typing import Any

from ._operation import Operation
from ..types import Schema, Record


class Insert(Operation):
    def insert(self, record: Record | list[Record] = None) -> 'Insert':
        self._refresh()

        self._query = 'INSERT '
        if record:
            if isinstance(record, list):
                for instance in record:
                    if isinstance(instance, Schema):
                        self.into(instance.__tablename__)
                        instance = dict(instance)
                    self.values(**instance)
            elif isinstance(record, Schema):
                self.into(record.__tablename__)
                self.values(**dict(record))
            elif isinstance(record, dict):
                self.values(**record)
        return self

    def into(self, table: str) -> 'Insert':
        if 'into' in self._query.lower():
            self.logger.warning('`INTO {tablename}` specified twice')  # noqa
        else:
            self._query += f"INTO {table} "
        return self

    # def values(self, *values: Any) -> 'Insert':
    def values(self, *values: Any, **columns: Any) -> 'Insert':
        if columns:
            self._query += f"({', '.join(columns.keys())}) "
            values = columns.values()
        placeholders = ', '.join([self._placeholder for i in range(len(values))])  # noqa
        if 'values' in self._query.lower():
            self._query += '\b, '
        self._qargs += values
        self._query += f"VALUES ({placeholders}) "
        return self
