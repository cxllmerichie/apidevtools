from apidevtools.simpleorm import Relation, Schema


class KindaShema(Schema):
    __tablename__ = 'ase'

    id: int
    another: type

    __relations__ = [
        Relation('item', dict(category_id='id'), type, 'items', type, ['*']),
        Relation('item', dict(category_id='another'), type, 'items', type, ['*']),
    ]

    @property
    def relations(self):
        return self.__relations__


s = KindaShema(**dict(id=1, another=dict))
print(s)
print(s.relations)
