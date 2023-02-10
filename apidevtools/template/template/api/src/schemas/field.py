from apidevtools import Schema


class FieldBase(Schema):
    __tablename__ = 'field'

    name: str
    value: str


class FieldCreate(FieldBase):
    ...


class FieldCreateCrud(FieldBase):
    item_id: int


class Field(FieldCreateCrud):
    id: int
