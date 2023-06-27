from typing import Any

from ._operation import Operation


class Select(Operation):
    def select(self, *columns: str) -> 'Select':
        self._refresh()

        c = self._constraint_wrapper
        _columns = ''
        for column in columns:
            _columns += f'{c}{column}{c}, '
        self._query = f"SELECT {_columns[:-2]} "
        return self
