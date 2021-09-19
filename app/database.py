from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi import Depends


SQLITE_DATABASE_URL = 'sqlite:///./db.db'

engine = create_engine(
    SQLITE_DATABASE_URL, connect_args={ 'check_same_thread': False }
)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)

Base = declarative_base(engine)