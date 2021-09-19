from fastapi import Query, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from . import get_db
from ..models import User


def user_by_token(
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter_by(token=token).first()

    if db_user is None:
        raise HTTPException(404, 'User not found')
    
    return db_user