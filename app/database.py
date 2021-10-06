from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import config

engine = create_engine(
    config.POSTGRESQL_DATABASE_URL, #connect_args={ 'check_same_thread': False }
)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)

Base = declarative_base(engine)