from typing import List, Optional

from pydantic import BaseModel, Field
from enum import Enum


class User(BaseModel):
    id:         int
    avatar:     str = Field(None, example='user.png')
    username:   str = Field(..., example='Alex123')

    class Config:
        orm_mode = True


class Chat(BaseModel):
    id: int
    name: str = Field(None, example='Бро')
    users: List[User]

    class Config:
        orm_mode = True


class Message(BaseModel):
    id:   int
    sender_id: int
    sender: User
    chat_id: int
    text: str = Field(..., example='Привет, друг! :D')

    class Config:
        orm_mode = True


class UpdateType(str, Enum):
    new = 'new'
    remove = 'remove'
    change = 'change'


class Update(BaseModel):
    message: Optional[Message] = None
    chat: Optional[Chat] = None
    type: UpdateType = UpdateType.new