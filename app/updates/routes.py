from typing import List, Optional

from .. import app
from .. import utils
from .. import schemas as global_schemas
from .. import models as global_models
from .sub_manager import SubManager

from fastapi import Depends, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import json


async def send_updates(ws: WebSocket, updates: List[global_schemas.Update]) -> bool:
    updates_json = json.dumps([update.dict() for update in updates])

    try:
        await ws.send_text(updates_json)
        return True
    except ConnectionClosed:
        return False


@app.get('/getUpdates', response_model=List[global_schemas.Update], tags=['Update'])
async def get_updates(
    db_user: global_models.User = Depends(utils.user_by_token)
):
    return SubManager.instance.waitQueueUpdates(db_user.id)


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

        updates = await SubManager.instance.waitQueueUpdates(db_user.id)
        await send_updates(ws, updates)

        while True:
            updates = await SubManager.instance.waitQueueUpdates(db_user.id, queue)
            
            if not await send_updates(ws, updates):
                break

    except WebSocketDisconnect:
        pass

    if queue is not None:
        SubManager.instance.delQueue(db_user.id, queue)