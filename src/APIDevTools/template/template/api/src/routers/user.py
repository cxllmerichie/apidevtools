from fastapi import APIRouter, Depends, HTTPException

from .. import crud, schemas


router = APIRouter(tags=['User'])


@router.post('/users/', name='Create user', response_model=dict)
async def _(user: schemas.UserCreate):
    db_user = await crud.get_user(email=user.email, schema=schemas.UserCreate)
    if db_user:
        raise HTTPException(status_code=400, detail=f'Email <{user.email}> already registered')
    db_user = await crud.create_user(user=user)
    return dict(**(await crud.create_token(user=db_user)), user=db_user.dict())


@router.put('/users/', name='Update my user', response_model=schemas.User)
async def _(user: schemas.UserUpdate,
            _user: schemas.User = Depends(crud.get_current_user)):
    db_user = await crud.update_user(user_id=_user.id, user=user)
    return db_user


@router.delete('/users/', name='Delete my user', status_code=200)
async def _(user: schemas.User = Depends(crud.get_current_user)):
    await crud.delete_user(user_id=user.id)
    return dict(detail=f'Successfully deleted user <{user.id}>')
