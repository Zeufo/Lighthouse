import asyncio
import time
import typing
from os import stat

from loguru import logger
from sqlalchemy.orm import exc
from telethon import TelegramClient
from tenacity import retry, stop_after_attempt, wait_fixed

from ai import WorkerAI
from config import CHANNELS, queue
from database import AsyncSessionLocal, NewsCRUD
from parser import TelethonParser
from services.format_service import TelethonCleaner
from services.news_service import analyze_daily_data, collect_news_cycle, send_digest_to_users


class Pipeline:
    @staticmethod
    async def process_news_and_save(client: TelegramClient) -> None:
        start = time.time()
        for channel in CHANNELS:
            await queue.put((collect_news_cycle, [channel, client], {}))

        logger.debug(f"collect news cycle took {int(time.time() - start)} seconds")
        await queue.join()

    @staticmethod
    async def analyze_daily_data() -> typing.Any:
        await queue.put((analyze_daily_data, [], {}))
        await queue.join()

    @staticmethod
    async def send_digest() -> None:
        await queue.put((send_digest_to_users, [], {}))
        await queue.join()

    @staticmethod
    async def is_connected() -> typing.Any:
        await queue.put((WorkerAI.say_hello, [], {}))
        await queue.join()

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10))
    async def _run_step(step_name: str, func, *args) -> None:
        logger.debug(f"Running step: {step_name}")
        await func(*args)

    @staticmethod
    async def run_full_cycle(client: TelegramClient) -> None:
        steps = [
            ("process_news", Pipeline.process_news_and_save, client),
            ("analyze", Pipeline.analyze_daily_data),
            ("send_digest", Pipeline.send_digest),
        ]

        for name, func, *args in steps:
            try:
                await Pipeline._run_step(name, func, *args)
            except Exception as e:
                logger.exception(f'Pipeline stopped at step "{name}"')
                # TODO: NOtify admin here
                return
