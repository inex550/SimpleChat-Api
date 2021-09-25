from typing import Union, Optional

from ..models import Chat, User
from ..schemas import Update
from .sub_manager import SubManager

from sqlalchemy.orm import Session


async def chat_notify(update: Update, chat: Union[int, Chat], db: Optional[Session] = None):
    if isinstance(chat, int):
        chat = db.query(Chat).get(chat)

    for user in chat.users:
        await SubManager.instance.notify(user.id, update)