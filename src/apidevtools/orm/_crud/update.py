from typing import Any

from ._operation import Operation


class Update(Operation):
    def __init__(self, table: str, instance=None):
        self._refresh()
        if instance:
            ...
        self._query = f"UPDATE {table} "

    def set(self, **values: Any) -> 'Update':
        values = ', '.join([f'{key} = {value}' for key, value in values.items()])
        self._query += f"SET {values} "
        return self
