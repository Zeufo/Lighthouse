import asyncio

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from telethon import TelegramClient

from bot import BOT
from config import API_HASH, API_ID, BOT_TOKEN, CHANNELS, TEST_LINK
from database import PostgresInit
from database.models import AsyncSessionLocal
from handlers import get_main_router
from parser import TelethonParser
from scheduler import Scheduler
from services import Pipeline
from services.news_service import send_digest_to_users
from services.worker import Worker
from utils import setup_logger, AntiSpamMiddleware


class MainProcess:
    @staticmethod
    async def Preparation(client: TelegramClient) -> None:
        try:
            setup_logger()
            await PostgresInit.create()

            is_empty = await PostgresInit.is_empty()
            logger.debug(is_empty)
            if is_empty:
                logger.info("Table is empty, start fill process...")
                logger.debug("Start parsing channels...")
                logger.debug("Parsed")

                await TelethonParser.parse_channels_status(client)
                channels_data = await TelethonParser.parse_channels_info(client)
                await PostgresInit.fill_channels_table(channels_data)

        except Exception as e:
            logger.exception("Error in preparation")

    @staticmethod
    async def Start(client: TelegramClient) -> None:
        try:
            logger.info("Start main process...")
            dp = Dispatcher()
            main_router = get_main_router()
            dp.include_router(main_router)
            dp.update.outer_middleware(AntiSpamMiddleware(1))
            asyncio.create_task(Worker.run())

            logger.info("worker is ready")
            await Scheduler.add_schedule(client)

            # await Pipeline.is_connected()  # TODO: think about to stop run if not
            # await Pipeline.process_news_and_save(client)
            # await Pipeline.analyze_daily_data()
            # await send_digest_to_users(0)
            #
            await dp.start_polling(BOT)

        except Exception as e:
            logger.exception("Error in start")
