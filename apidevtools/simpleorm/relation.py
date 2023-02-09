from .schema import Schema


class Relation:
    columns: list[str] = ['*']
    tablename: str
    where: dict
    ext_schema_t: type[Schema]
    fieldname: str
    rel_schema_t: type[Schema] = None
