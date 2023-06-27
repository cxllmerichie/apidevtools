from typing import Any

from ._operation import Operation


class Insert(Operation):
    def insert(self, instance=None) -> 'Insert':
        self._refresh()

        if instance:
            ...
        self._query = 'INSERT '
        return self

    def into(self, table: str) -> 'Insert':
        self._query += f"INTO {table} "
        return self

    # def values(self, *values: Any) -> 'Insert':
    def values(self, *values: Any, **columns: Any) -> 'Insert':
        # if columns:
        #     self._query += f"({', '.join(columns.keys())}) "
        #     values = columns.values()
        placeholders = ', '.join([self._placeholder for i in range(len(values))])
        self._qargs += values
        self._query += f"VALUES ({placeholders}) "
        return self
