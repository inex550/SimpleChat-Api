from fastapi import APIRouter


router = APIRouter(
    tags=['Chat'],
    prefix='/chat'
)

from . import routes