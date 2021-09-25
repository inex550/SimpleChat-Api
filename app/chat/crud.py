from typing import List

from sqlalchemy.orm import Session

from .. import models


def create_chat(db: Session, name: str = None) -> models.Chat:
    chat = models.Chat(name=name)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def create_chat_assotioations(db: Session, chat: models.Chat, users: List[int], creator: models.User):
    assotioation_insert = models.chat_users_table.insert()

    db.execute(assotioation_insert.values(
        chat_id = chat.id,
        user_id = creator.id
    ))

    users = set(users)
    
    if creator.id in users:
        users.remove(creator.id)

    for user_id in users:
        db.execute(assotioation_insert.values(
            chat_id = chat.id,
            user_id = user_id
        ))

    db.commit()


def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter_by(username=username).first()