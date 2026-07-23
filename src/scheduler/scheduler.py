import abc
import time
import typing
from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(
    func,
    trigger="cron",
    hour=?,
    minute=?,
    id = what_prog_do,

)


scheduler.add_job(
    func,
    trigger="cron",
    hour=?,
    minute=?,
    id = what_prog_do,

)
class Scheduler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def schedule() -> None:
        pass
