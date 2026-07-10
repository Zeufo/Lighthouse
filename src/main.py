# TODO: Put it in Docker IDK
import asyncio

from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, CHANNELS, TEST_LINK
from run import MainProcess


async def main() -> None:
    async with TelegramClient("news_parser", API_ID, API_HASH) as client:  # type:ignore
        await MainProcess.Preparation()


try:
    asyncio.run(main())

except KeyboardInterrupt:
    logger.critical("Keyboard Interrupt!")
