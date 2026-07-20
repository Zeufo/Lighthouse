import asyncio

from format_service import TelethonCleaner
from loguru import logger
from telethon import TelegramClient

from config import CHANNELS, queue
from parser import TelethonParser


async def full_news_cycle(channel: str, client: TelegramClient) -> None:
    try:
        news = await TelethonParser.parse_today_news(channel, client)
        if news is None:
            return

        news = await TelethonCleaner.clean(news)

    except Exception as e:
        logger.exception(f"Error in processing {news}")


class Pipeline:
    @staticmethod
    async def process_news_and_save(client: TelegramClient) -> None:
        for channel in CHANNELS:
            await queue.put((full_news_cycle, [channel, client], {}))
