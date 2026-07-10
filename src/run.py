import asyncio

from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, CHANNELS, TEST_LINK
from database import PostgresInit
from parser import TelethonParser
from utils import setup_logger


class MainProcess:
    @staticmethod
    async def Preparation() -> None:
        setup_logger()
        await PostgresInit.create()

        is_empty = await PostgresInit.is_empty()
        logger.debug(is_empty)
        if is_empty:  # Not implemented yet
            logger.info("Table is empty, start fill process...")
            # await PostgresInit.fill_channels_table()
            # TODO: fill table func here

        logger.debug("Start parsing channels...")
        await TelethonParser.parse_channels_info()

    @staticmethod
    async def Start(self) -> None:
        pass
