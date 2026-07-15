import asyncio
import typing

from loguru import logger

from config import queue


class Worker:
    @staticmethod
    async def run() -> typing.Any:
        while True:
            func, arg, kwargs = await queue.get()
            test_obj = await func(*arg, **kwargs)
            logger.debug(f"test_obj is {test_obj}")
            queue.task_done()
