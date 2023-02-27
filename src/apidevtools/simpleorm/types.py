from typing import Any

from .schema import Schema


Instance = dict[str, Any] | Schema
SchemaType = type[dict[str, Any] | Schema]
Record = dict[str, Any] | Schema | None
