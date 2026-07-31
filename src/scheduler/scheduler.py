import abc
import time
import typing
from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger

from services.pipeline import Pipeline


class Scheduler:
    @staticmethod
    @abc.abstractmethod
    async def add_schedule(client) -> None:
        my_scheduler = AsyncIOScheduler(timezone="Europe/Samara")
        my_scheduler.add_job(
            Pipeline.run_full_cycle,
            trigger="cron",
            hour=19,
            minute=30,
            args=(client,),
        )

        my_scheduler.start()

        logger.info("Scheduler is ready")
