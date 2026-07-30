import abc
import time
import typing
from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from services.pipeline import Pipeline

my_scheduler = BackgroundScheduler(timezone="UTC")
# my_scheduler.add_job(
#    Pipeline.run_full_cycle,
#    trigger="cron",
#    hour=1,
#    minute=1,
# args=(client,),
# )


class Scheduler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def schedule() -> None:
        pass
