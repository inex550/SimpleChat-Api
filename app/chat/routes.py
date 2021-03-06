from app.updates import notifiers
from typing import List, Optional

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
def get_chat_messages(
    chat_id: int,
    start: Optional[int] = None,
    batch: Optional[int] = None,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    messages_filter = db.query(global_models.Message).filter_by(chat_id = chat_id).order_by(global_models.Message.id.desc())

    if start is not None:
        messages_filter = messages_filter.filter(global_models.Message.id <= start)

    if batch is not None:
        messages_filter = messages_filter.limit(batch)

    return messages_filter.all()[::-1]


@router.post('/{chat_id}/sendMessage', response_model=global_schemas.Message)
async def send_message(
    chat_id: int,
    send_message: schemas.SendMessage,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
): 
    message = global_models.Message(
        text=send_message.text,
        sender=db_user,
        chat_id=chat_id
    )

    db.add(message)
    db.commit()

    await notifiers.chat_notify(global_schemas.Update(message=message, type=global_schemas.UpdateType.new), chat_id, db)
    return message


@router.post('/new', response_model=global_schemas.Chat)
async def craete_chat(
    new_chat: schemas.NewChat,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    chat = crud.create_chat(db, new_chat.name)
    crud.create_chat_assotioations(db, chat, new_chat.users, db_user)

    await notifiers.chat_notify(global_schemas.Update(chat=chat, type=global_schemas.UpdateType.new), chat, db)

    return chat


@router.post('/newPrivate', response_model=global_schemas.Chat)
async def create_private_chat(
    new_chat: schemas.NewPrivateChat,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    if new_chat.username == db_user.username:
        raise HTTPException(400, "???????????? ?????????????? ?????? ?? ?????????? ??????????")

    chat = crud.create_chat(db)
    user = crud.get_user_by_username(db, new_chat.username)

    if user is None:
        raise HTTPException(404, '???????????????????????? ?? ?????????? ?????????? ???? ????????????')
    
    crud.create_chat_assotioations(db, chat, [user.id], db_user)

    await notifiers.chat_notify(global_schemas.Update(chat=chat, type=global_schemas.UpdateType.new), chat, db)

    return chat


@router.delete('/{chat_id}')
async def delete_chat(
    chat_id: int,
    db: Session = Depends(utils.get_db),
    db_user: global_models.User = Depends(utils.user_by_token)
):
    chat = db.query(global_models.Chat).get(chat_id)

    if chat is None or chat not in db_user.chats:
        raise HTTPException(404, '?????? ???? ????????????')

    db.query(global_models.Message).filter_by(chat=chat).delete()
    db.commit()

    await notifiers.chat_notify(global_schemas.Update(chat=chat, type=global_schemas.UpdateType.remove), chat, db)

    db.delete(chat)
    db.commit()

    return { 'ok': True }