from typing import Any

from ._operation import Operation
from ..types import Schema, Record


class Insert(Operation):
    def insert(self, record: Record | list[Record] = None) -> 'Insert':
        self._commands['insert'] = 'INSERT'
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
        self._commands['into'] = f"INTO {table}"
        return self

    def values(self, *values: Any, **columns: Any) -> 'Insert':
        if columns:
            self._commands['columns'] = f"({', '.join(columns.keys())})"
            values = columns.values()
        if self._commands.get('values'):
            self._commands['values'] += f"'\b, '({', '.join(columns.keys())})"
        self._args += values
        placeholders = ', '.join([self._placeholder for i in range(len(values))])  # noqa
        self._commands['values'] = f"VALUES ({placeholders})"
        return self
