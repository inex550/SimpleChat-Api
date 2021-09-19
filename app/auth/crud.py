from sqlalchemy.orm import Session
import secrets

from . import schemas
from .. import models
from ..utils import get_password_hash


def get_user_by_auth_model(db: Session, model: schemas.AuthUser):
    return db.query(models.User).filter_by(
        username = model.username,
        hashed_password = get_password_hash(model.password)
    ).first()


def check_user_exist(db: Session, username: str) -> bool:
    return db.query(models.User).filter_by(
        username = username
    ).first() is not None


def create_user_by_auth_model(db: Session, model: schemas.AuthUser):
    db_user = models.User(
        username = model.username,
        hashed_password = get_password_hash(model.password),
        token = secrets.token_hex(16) 
    )

    db.add(db_user)
    db.commit()

    db.refresh(db_user)

    return db_user