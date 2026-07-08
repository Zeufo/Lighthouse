import abc
import time
import typing
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def schedule() -> None:
        pass
