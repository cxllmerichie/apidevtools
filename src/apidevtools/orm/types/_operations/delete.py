from ._operation import Operation
from ..types import Schema, Record


class Delete(Operation):
    def delete(self, record: Record = None) -> 'Delete':
        self._commands['delete'] = 'DELETE'
        if isinstance(record, Schema):
            self.fr0m(record.__tablename__)
            self.where(**{record.__primary__: record.__getattribute__(record.__primary__)})
            return self
        elif isinstance(record, dict):
            self.where(**record)
        return self
    