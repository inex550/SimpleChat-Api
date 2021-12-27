from fastapi import FastAPI


app = FastAPI(
    title='Messenger Api'
)

from . import auth
from . import chat
from . import user
from . import media

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(user.router)
app.include_router(media.router)