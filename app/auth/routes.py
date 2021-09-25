from . import router, crud
from . import schemas as user_schemas
from ..utils import get_db

from fastapi import Depends, HTTPException


@router.post('/login', response_model=user_schemas.UserIdentifers)
def user_login(
    user: user_schemas.AuthUser,
    db = Depends(get_db)
): 
    db_user = crud.get_user_by_auth_model(db, user)

    if db_user is None:
        raise HTTPException(404, 'Пользователь не найден')

    return db_user


@router.post('/register', response_model=user_schemas.UserIdentifers)
def user_register(
    user: user_schemas.AuthUser,
    db = Depends(get_db)
): 
    if crud.check_user_exist(db, user.username):
        raise HTTPException(409, 'Пользователь с таким ником уже зарегистрирован')

    db_user = crud.create_user_by_auth_model(db, user)
    return db_user