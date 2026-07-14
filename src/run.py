import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, BOT_TOKEN, CHANNELS, TEST_LINK
from database import PostgresInit
from database.models import AsyncSessionLocal
from handlers import get_main_router
from parser import TelethonParser
from utils import setup_logger


class MainProcess:
    @staticmethod
    async def Preparation(client: TelegramClient) -> None:
        try:
            setup_logger()
            await PostgresInit.create()

            is_empty = await PostgresInit.is_empty()
            logger.debug(is_empty)
            if is_empty:  # Not implemented yet
                logger.info("Table is empty, start fill process...")
                # await PostgresInit.fill_channels_table()
                # TODO: fill table func here

            logger.debug("Start parsing channels...")

            # await TelethonParser.parse_channels_status(client)
            # channels_data = await TelethonParser.parse_channels_info(client)
            # await PostgresInit.fill_channels_table(channels_data)
        except Exception as e:
            logger.exception("Error in preparation")

    @staticmethod
    async def Start(client: TelegramClient) -> None:
        local_session = AsyncSessionLocal
        dp = Dispatcher()
        dp["alchemy_session"] = local_session
        main_router = get_main_router()
        dp.include_router(main_router)
        bot = Bot(token=BOT_TOKEN)  # type: ignore
        logger.info("Bot is ready")
        await dp.start_polling(bot)
