import abc
import typing

from loguru import logger
from sqlalchemy import text
from telethon import TelegramClient
from telethon.errors import ChannelInvalidError
from telethon.tl.types import channels

from .models import AsyncSessionLocal, Base, engine


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
                logger.debug("Connection confirmed")
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
                    return False

            return True

        except Exception as e:
            logger.error("Error in Checking tables...", e)
            raise RuntimeError

    @staticmethod
    async def fill_channels_table(to_insert: list) -> None:
        async with AsyncSessionLocal() as session:
            query = text("""INSERT INTO channels (
                channel_id, 
                channel_title, 
                channel_status,
                subscribers, 
                last_parsed_at, 
                last_updated_at) VALUES (

                :channel_id, 
                :channel_title, 
                :channel_status, 
                :subscribers, 
                :last_parsed_at, 
                :last_updated_at
                )""")

            await session.execute(query, params=to_insert)
            await session.commit()

    @staticmethod
    async def fill_users_table(tg_session: TelegramClient) -> None:
        async with AsyncSessionLocal() as session:
            query = text("""INSERT INTO Users (
                user_id, 
                created_at) VALUES (

                ) """)
            data = []  # Under constract
            await session.execute(query, params=data)

    @staticmethod
    async def fill_news_table(tg_session: TelegramClient) -> None:
        async with AsyncSessionLocal() as session:
            query = text("""INSERT INTO News (
                channel_id, 
                channel_title, 
                text, 
                views, 
                published_at) VALUES (

                ) """)
            data = []  # Under constract
            await session.execute(query, params=data)

            await session.commit()
