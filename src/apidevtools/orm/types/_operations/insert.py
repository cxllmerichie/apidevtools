from typing import Any

from ._operation import Operation
from ..types import Schema, Record


class Insert(Operation):
    def insert(self, record: Record | list[Record] = None) -> 'Insert':
        self._commands['insert'] = 'INSERT'
        if record:
            if isinstance(record, list):
                self.insert(record)
            elif isinstance(record, Schema):
                self.into(record.__tablename__)
                self.values(**dict(record))
            elif isinstance(record, dict):
                self.values(**record)
        return self

    def into(self, table: str) -> 'Insert':
        self._commands['into'] = f"INTO {table}"
        return self

    def values(self, **columns: Any) -> 'Insert':
        self._commands['columns'] = f"({', '.join(columns.keys())})"
        self._args += (values := columns.values())
        placeholders = ', '.join([self._placeholder for i in range(len(values))])  # noqa
        if self._commands.get('values'):
            self._commands['values'] += f", ({placeholders})"
        else:
            self._commands['values'] = f"VALUES ({placeholders})"
        return self
