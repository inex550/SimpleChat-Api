from typing import Dict, List, Optional
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

    async def waitQueueUpdates(self, userId, queue: Optional[Queue] = None) -> List[Update]:
        updates: List[Update] = []

        default_queue = self.getDefaultQueue(userId)

        if queue is None:
            queue = default_queue
        else:
            updates.append(await queue.get())

        for _ in range(queue.qsize()):
            updates.append(await queue.get())

        if (queue is not default_queue):
            for _ in range(default_queue.qsize()):
                await default_queue.get()

        return updates

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