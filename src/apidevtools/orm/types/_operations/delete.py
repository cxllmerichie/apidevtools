from ._operation import Operation
from ..types import Schema, Record


class Delete(Operation):
    def delete(self, instance: Record = None) -> 'Delete':
        self._refresh()

        if isinstance(instance, Schema):
            self.fr0m(instance.__tablename__)
            key = instance.__primary__
            self.where(**{key: instance.__getattribute__(key)})
            self.where()
            return self
        self._query = 'DELETE '
        return self
    