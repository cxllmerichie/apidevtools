from apidevtools import inf

from .. import schemas
from ..const import db
from .item import get_items, delete_item


async def create_category(user_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    category = schemas.CategoryCreateCrud(**dict(category), user_id=user_id)
    db_category = await db.insert(category, schemas.Category)
    return db_category


async def get_category(category_id: int, schema: type = schemas.Category) -> schemas.Category | None:
    query, args = f'SELECT * FROM "category" WHERE "id" = $1;', (category_id, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def get_categories(user_id: int, limit: int = inf, offset: int = 0, schema: type = schemas.Category) -> list[schemas.Category]:
    query, args = f'SELECT * FROM "category" WHERE "user_id" = $1 LIMIT $2 OFFSET $3;', (user_id, limit, offset)
    db_user = (await db.select(query, args, schema)).all()
    return db_user


async def update_category(category_id: int, category: schemas.CategoryCreate) -> schemas.Category:
    db_user = await db.update(category, dict(id=category_id), schemas.Category)
    return db_user


async def delete_category(category_id: int) -> None:
    db_items = await get_items(category_id=category_id, schema=schemas.Item)
    for db_item in db_items:
        await delete_item(item_id=db_item.id)
    query, args = f'DELETE FROM "category" WHERE "id" = $1;', (category_id, )
    await db.execute(query, args)
