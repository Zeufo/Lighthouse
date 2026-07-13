# TODO: Put it in Docker IDK
import asyncio

from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID
from run import MainProcess


async def main() -> None:
    async with TelegramClient("news_parser", API_ID, API_HASH) as client:  # type:ignore
        await MainProcess.Preparation(client)
        await MainProcess.Start(client)


try:
    asyncio.run(main())

except KeyboardInterrupt:
    logger.critical("Keyboard Interrupt!")
