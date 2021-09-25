from .database import Base

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime


chat_users_table = Table('chat_users', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('chat_id', ForeignKey('chats.id'), index=True),
    Column('user_id', ForeignKey('users.id'), index=True)
)


class User(Base):
    __tablename__ = 'users'

    id =                Column(Integer, primary_key=True)
    token =             Column(String, nullable=False, unique=True, index=True)
    username =          Column(String, nullable=False, unique=True, index=True)
    hashed_password =   Column(String, nullable=False)

    chats = relationship('Chat', secondary=chat_users_table, back_populates='users')


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    users = relationship('User', secondary=chat_users_table, back_populates='chats')
    messages = relationship('Message', back_populates='chat')


class Message(Base):
    __tablename__ = 'messages'

    id =        Column(Integer, primary_key=True)
    text =      Column(String, nullable=False)
    date =      Column(DateTime, nullable=False, default=datetime.now)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id =   Column(Integer, ForeignKey('chats.id'), nullable=False)

    sender = relationship('User')
    chat = relationship('Chat', back_populates='messages')