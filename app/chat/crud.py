from typing import List

from sqlalchemy.orm import Session

from .. import models


def create_chat(db: Session, name: str = None) -> models.Chat:
    chat = models.Chat(name=name)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def create_chat_assotioations(db: Session, chat: models.Chat, users: List[int]):
    assotioation_insert = models.chat_users_table.insert()

    for user_id in users:
        assotioation_insert.values(
            chat_id = chat.id,
            user_id = user_id
        )

    db.commit()