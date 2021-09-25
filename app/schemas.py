from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    id:   int
    sender_id: int
    chat_id: int
    text: str = Field(..., example='Привет, друг! :D')

    class Config:
        orm_mode = True


class User(BaseModel):
    id:         int
    username:   str = Field(..., example='Alex123')

    class Config:
        orm_mode = True


class Chat(BaseModel):
    id: int
    name: str = Field(None, example='Бро')
    users: List[User]

    class Config:
        orm_mode = True


class Update(BaseModel):
    message: Optional[Message] = None