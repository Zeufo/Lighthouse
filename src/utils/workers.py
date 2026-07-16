import asyncio
import typing

from loguru import logger

from ai import WorkerAI
from config import queue


class Worker:
    @staticmethod
    async def run() -> typing.Any:
        while True:
            func, arg, kwargs = await queue.get()
            await func(*arg, **kwargs)
            queue.task_done()
