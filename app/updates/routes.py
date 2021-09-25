from typing import List, Optional

from .. import app
from .. import utils
from .. import schemas as global_schemas
from .. import models as global_models
from .sub_manager import SubManager

from sqlalchemy.orm import Session
from fastapi import Depends, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import asyncio
import json


async def get_queue_updates(queue: asyncio.Queue):
    updates = [await queue.get()]

    for _ in range(queue.qsize()):
        updates.append(await queue.get())

    return updates


@app.get('/getUpdates', response_model=List[global_schemas.Update], tags=['Update'])
async def get_updates(
    db_user: global_models.User = Depends(utils.user_by_token)
):
    queue = SubManager.instance.getDefaultQueue(db_user.id)
    return get_queue_updates(queue)


@app.websocket('/getUpdates')
async def get_updates_ws(
    ws: WebSocket,
    db_user: global_models.User = Depends(utils.user_by_token_ws)
):
    if db_user is None: return

    queue = None

    try:
        await ws.accept()

        queue = SubManager.instance.newQueue(db_user.id)

        while True:
            updates = await get_queue_updates(queue)
            updates_json = json.dumps([update.dict() for update in updates])

            try:
                await ws.send_text(updates_json)
            except ConnectionClosed:
                break

    except WebSocketDisconnect:
        pass

    if queue is not None:
        SubManager.instance.delQueue(db_user.id, queue)