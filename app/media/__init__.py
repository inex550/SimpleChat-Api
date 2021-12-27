from fastapi import APIRouter

router = APIRouter(
    tags=['Media']
)

from . import routes