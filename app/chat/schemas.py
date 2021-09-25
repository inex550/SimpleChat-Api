from typing import List

from pydantic import BaseModel, Field


class NewChat(BaseModel):
    name: str = Field(None, example='Новый чат :D')
    users: List[int]


class SendMessage(BaseModel):
    text: str


class NewPrivateChat(BaseModel):
    username: str = Field(None, example='Alex123')