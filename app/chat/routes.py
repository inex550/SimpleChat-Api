from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from . import router, schemas, crud
from .. import utils
from .. import schemas as global_schemas
from .. import models as global_models


@router.get('/my', response_model=List[global_schemas.Chat])
def get_user_chats(
    db_user: global_models.User = Depends(utils.user_by_token),
): return db_user.chats


@router.get('/{chat_id}/messages', response_model=List[global_schemas.Message])
def chat_messages(
    chat_id: int,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    assotioation_entry = db.query(global_models.chat_users_table).filter_by(
        user_id = db_user.id,
        chat_id = chat_id
    ).first()

    if assotioation_entry is None:
        raise HTTPException(404, 'Chat not exists')

    return db.query(global_models.Chat).get(chat_id)


@router.post('/new', response_model=global_schemas.Chat)
def craete_chat(
    new_chat: schemas.NewChat,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    chat = crud.create_chat(db, new_chat.name)
    crud.create_chat_assotioations(db, chat, new_chat.users)

    return chat