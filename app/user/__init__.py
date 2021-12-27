from fastapi import APIRouter

router = APIRouter(
    prefix='/user',
    tags=['User']
)

from . import routes