from typing import Any

from ._operation import Operation


class Select(Operation):
    def __init__(self, *columns: str):
        self._refresh()

        c = self.connector.constraint_wrapper
        _columns = ''
        for column in columns:
            _columns += f'{c}{column}{c}, '
        self._query = f"SELECT {_columns[:-2]} "

