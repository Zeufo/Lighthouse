import asyncio

from loguru import logger
from telethon import TelegramClient

from config import CHANNELS


async def ping_channels() -> bool:
    async with TelegramClient("news_parser", API_ID, API_HASH) as client:  # type:ignore
        logger.info("Started pinging channels...")
        for channel in CHANNELS:
            try:


            except Exception as e:
