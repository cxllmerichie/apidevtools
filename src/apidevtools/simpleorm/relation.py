class Relation:
    def __init__(self, tablename: str, where: dict, ext_schema_t: type, fieldname: str,
                 rel_schema_t: type = dict, columns: list[str] = None):
        self.tablename: str = tablename
        self.where: dict = where
        self.ext_schema_t: type = ext_schema_t
        self.fieldname: str = fieldname
        self.rel_schema_t: type = rel_schema_t
        self.columns: list[str] = columns if columns else ['*']
