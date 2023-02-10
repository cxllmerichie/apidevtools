from fastapi import APIRouter, Depends, HTTPException
from apidevtools import inf

from .. import crud, schemas


router = APIRouter(tags=['Category'])


@router.post('/categories/', name='Create category', response_model=schemas.Category)
async def _(category: schemas.CategoryCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.create_category(user_id=user.id, category=category)
    return db_category


@router.get('/categories/{category_id}/', name='Get category by id', response_model=schemas.Category)
async def _(category_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_category = await crud.get_category(category_id=category_id)
    return db_category


@router.get('/categories/', name='Get all categories of my user', response_model=schemas.Category)
async def _(limit: int = inf, offset: int = 0, user: schemas.User = Depends(crud.get_current_user)):
    db_categories = await crud.get_categories(user_id=user.id, limit=limit, offset=offset)
    return db_categories


@router.put('/categories/', name='Update category by id', response_model=schemas.Category)
async def _(category_id: int, category: schemas.CategoryCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_category(category_id=category_id, category=category)
    return db_user


@router.delete('/categories/', name='Delete category by id', status_code=200)
async def _(category_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_category(category_id=category_id)
    return dict(detail=f'Successfully deleted category <{category_id}>')
