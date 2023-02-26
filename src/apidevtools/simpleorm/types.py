from typing import Any

from .schema import Schema


Instance = dict | Schema
SchemaType = type[dict | Schema]
Record = dict[str, Any] | Schema | None
