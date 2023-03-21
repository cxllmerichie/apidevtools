from typing import Any


class Relation:
    def __init__(self, tablename: str, where: dict[str, Any], ext_schema_t: 'SchemaType', fieldname: str,
                 rel_schema_t: 'SchemaType' = dict, columns: list[str] = None):
        self.tablename: str = tablename
        self.where: dict[str, Any] = where
        self.ext_schema_t: 'SchemaType' = ext_schema_t
        self.fieldname: str = fieldname
        self.rel_schema_t: 'SchemaType' = rel_schema_t
        self.columns: list[str] = columns if columns else ['*']
