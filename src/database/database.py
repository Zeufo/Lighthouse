import abc
import typing

from loguru import logger
from sqlalchemy import text
from telethon import TelegramClient

from database import AsyncSessionLocal, Base, engine


class DatabaseInit(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def create(*args, **kwargs) -> None:
        pass


@typing.final
class PostgresInit(DatabaseInit):
    @staticmethod
    async def create() -> None:
        try:
            logger.info("Creating the table...")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                await conn.commit()
                await conn.close()
                logger.info("Tables created")

        except Exception as e:
            logger.error("Error in table creation", e)
            raise RuntimeError

    @staticmethod
    async def is_empty() -> bool:
        try:
            logger.info("Checking if the table is empty...")
            async with AsyncSessionLocal() as session:
                result = await session.execute(text("SELECT EXISTS (SELECT 1 FROM channels);"))
                if result.scalar():
                    return True

            return False

        except Exception as e:
            logger.error("Error in Checking tables...", e)
            raise RuntimeError

    @staticmethod
    async def fill_channels_table(tg_session: TelegramClient) -> None:
        pass
