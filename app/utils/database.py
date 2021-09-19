from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal


def get_db() -> Session:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()