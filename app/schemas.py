from typing import List

from pydantic import BaseModel, Field


class Message(BaseModel):
    id:   int
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
    name: str = Field(..., example='Бро')
    users: List[User]

    class Config:
        orm_mode = True

