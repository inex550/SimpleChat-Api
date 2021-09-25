from typing import Dict, List
from asyncio import Queue

from ..schemas import Update


class SubManager:

    instance: 'SubManager'

    def __init__(self):
        self._user_queues: Dict[int, List[Queue]] = {}

    async def notify(self, userId: int, update: Update):
        queues_list = self._user_queues.setdefault(userId, [Queue()])

        for queue in queues_list:
            await queue.put(update)

    def getDefaultQueue(self, userId):
        return self._user_queues.setdefault(userId, [Queue()])[0]

    def newQueue(self, userId) -> Queue: 
        queue = Queue()
        self._user_queues.setdefault(userId, [Queue()]).append(queue)
        return queue

    def delQueue(self, userId, queue):
        queues_list = self._user_queues.get(userId)

        if queues_list is not None:
            queues_list.remove(queue)


SubManager.instance = SubManager()