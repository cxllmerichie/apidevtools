from fastapi import APIRouter, Depends, HTTPException
from apidevtools import inf

from .. import crud, schemas


router = APIRouter(tags=['Item'])


@router.post('/items/', name='Create item', response_model=schemas.Item)
async def _(category_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.create_item(category_id=category_id, item=item)
    return db_item


@router.get('/items/{item_id}/', name='Get item by id', response_model=schemas.Item)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_item = await crud.get_item(item_id=item_id)
    return db_item


@router.get('/items/', name='Get all items by category id', response_model=schemas.Item)
async def _(category_id: int, limit: int = inf, offset: int = 0,
            user: schemas.User = Depends(crud.get_current_user)):
    db_items = await crud.get_items(category_id=category_id, limit=limit, offset=offset)
    return db_items


@router.put('/items/', name='Update item by id', response_model=schemas.Item)
async def _(item_id: int, item: schemas.ItemCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_item(item_id=item_id, item=item)
    return db_user


@router.delete('/items/', name='Delete item by id', status_code=200)
async def _(item_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_item(item_id=item_id)
    return dict(detail=f'Successfully deleted item <{item_id}>')
