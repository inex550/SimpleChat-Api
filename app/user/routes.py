from typing import List

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from os import path

from . import router
from ..utils.token import user_by_token, get_db
from ..media import utils
from .. import (
    models as global_models,
    schemas as global_schemas
)


@router.post('/username/change')
def change_username(
    username: str = Query(...),
    db: Session = Depends(get_db),
    db_user: global_models.User = Depends(user_by_token)
):
    if db.query(global_models.User).filter_by(username=username).first() != None:
        raise HTTPException(400, 'Данный ник уже занят')

    db_user.username = username
    db.commit()

    return { 'ok': True }


@router.post('/avatar/change')
def change_avatar(
    avatar: str = Query(...),
    db: Session = Depends(get_db),
    db_user: global_models.User = Depends(user_by_token)
):
    if not path.exists(path.join(utils.base_img_path, avatar)):
        raise HTTPException(404, 'Image not found')

    db_user.avatar = avatar
    db.commit()

    return { 'ok': True }


@router.get('/search', response_model=List[global_schemas.User])
def search_user(
    query: str = Query(...),
    db: Session = Depends(get_db),
    db_user: global_models.User = Depends(user_by_token)
):
    if query == '':
        return []

    users = db.query(global_models.User).filter(
        global_models.User.username.like(f'{query}%'),
        global_models.User.id != db_user.id
    ).all()

    return users
