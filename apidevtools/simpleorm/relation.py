class Relation:
    def __init__(self, tablename: str, where: dict, ext_schema_t: type['Schema'], fieldname: str,
                 columns: list[str] = ['*'], rel_schema_t: type['Schema'] = None):
        self.columns: list[str] = columns
        self.tablename: str = tablename
        self.where: dict = where
        self.ext_schema_t: type['Schema'] = ext_schema_t
        self.fieldname: str = fieldname
        self.rel_schema_t: type['Schema'] = rel_schema_t
