from apidevtools import inf, Relation

from .. import schemas
from ..const import db
from .field import get_fields, delete_field


async def create_item(user_id: int, item: schemas.ItemCreate) -> schemas.Item:
    item = schemas.ItemCreateCrud(**dict(item), user_id=user_id)
    db_item = await db.insert(item, schemas.Item)
    return db_item


async def get_item(item_id: int, schema: type = schemas.Item) -> schemas.Item | None:
    query, args = f'SELECT * FROM "item" WHERE "id" = $1;', (item_id, )
    db_item = (await db.select(query, args, schema, True)).first()
    return db_item


async def get_items(user_id: int, limit: int = inf, offset: int = 0, schema: type = schemas.Item) -> list[schemas.Item]:
    query, args = f'SELECT * FROM "item" WHERE "user_id" = $1 LIMIT $2 OFFSET $3;', (user_id, limit, offset)
    db_items = (await db.select(query, args, schema)).all()
    return db_items


async def update_item(item_id: int, item: schemas.ItemCreate) -> schemas.Item:
    db_item = await db.update(item, dict(id=item_id), schemas.Item)
    return db_item


async def delete_item(item_id: int) -> None:
    db_fields = await get_fields(item_id=item_id)
    for db_field in db_fields:
        await delete_field(field_id=db_field.id)
    query, args = f'DELETE FROM "item" WHERE "id" = $1;', (item_id, )
    await db.execute(query, args)
