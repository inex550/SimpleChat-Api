from fastapi import FastAPI


app = FastAPI(
    title='Messenger Api'
)

from . import chat
from . import auth

app.include_router(chat.router)
app.include_router(auth.router)