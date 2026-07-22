import asyncio
import time
import typing

from loguru import logger
from telethon import TelegramClient

from ai import WorkerAI
from config import CHANNELS, queue
from database import AsyncSessionLocal, NewsCRUD
from parser import TelethonParser
from services.format_service import TelethonCleaner
from services.news_service import collect_news_cycle


async def daily_data_service() -> None:
    pass


class Pipeline:
    @staticmethod
    async def process_news_and_save(client: TelegramClient) -> None:
        for channel in CHANNELS:
            await queue.put((collect_news_cycle, [channel, client], {}))

        await queue.join()

    @staticmethod
    async def analyze_daily_data() -> typing.Any:
        await queue.put(daily_data_service)
