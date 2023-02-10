from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['Field'])


@router.post('/fields/', name='Add new field to item by id', response_model=schemas.Field)
async def _(item_id: int, field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.create_field(user_id=user.id, field=field)
    return db_field


@router.get('/fields/{field_id}/', name='Get field by id', response_model=schemas.Field)
async def _(field_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    db_field = await crud.get_field(field_id=field_id)
    return db_field


@router.put('/fields/', name='Update field by id', response_model=schemas.Field)
async def _(field_id: int, field: schemas.FieldCreate,
            user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_field(field_id=field_id, field=field)
    return db_user


@router.delete('/fields/', name='Delete field by id', status_code=200)
async def _(field_id: int,
            user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_field(field_id=field_id)
    return dict(detail=f'Successfully deleted field <{field_id}>')
