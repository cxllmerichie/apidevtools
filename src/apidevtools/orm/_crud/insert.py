from typing import Any

from ._operation import Operation


class Insert(Operation):
    def __init__(self, instance=None):
        self._refresh()

        if instance:
            ...
        self._query = 'INSERT '

    def into(self, table: str) -> 'Insert':
        self._query += f"INTO {table} "
        return self

    # def values(self, *values: Any) -> 'Insert':
    def values(self, *values: Any, **columns: Any) -> 'Insert':
        # if columns:
        #     self._query += f"({', '.join(columns.keys())}) "
        #     values = columns.values()
        self._query += f"VALUES {', '.join(values)} "
        return self
