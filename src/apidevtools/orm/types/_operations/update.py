from typing import Any

from ._operation import Operation


class Update(Operation):
    def update(self, table: str, instance=None) -> 'Update':
        self._refresh()
        if instance:
            ...
        self._query = f"UPDATE {table} "
        return self

    def set(self, **values: Any) -> 'Update':
        values = ', '.join([f'{key} = {value}' for key, value in values.items()])
        self._query += f"SET {values} "
        return self
