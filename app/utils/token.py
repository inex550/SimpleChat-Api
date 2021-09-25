from fastapi import Query, Depends, WebSocket
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
        raise HTTPException(404, 'Недействительный токен')
    
    return db_user


async def user_by_token_ws(
    ws: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter_by(token=token).first()

    if db_user is None:
        await ws.accept()
        await ws.send_json({'detail': 'Пользователь не найден'})
        await ws.close()
    
    return db_user