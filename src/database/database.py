import abc
import typing
from datetime import datetime

from loguru import logger
from sqlalchemy import text
from telethon import TelegramClient
from telethon.errors import ChannelInvalidError
from telethon.tl.types import channels

from .models import AsyncSessionLocal, Base, News, engine


class DatabaseInit(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def create(*args, **kwargs) -> None:
        pass


@typing.final
class NewsCRUD:
    @staticmethod
    async def save_after_collect(to_insert: dict) -> None:
        async with AsyncSessionLocal() as session:
            # in construct
            query = text("""INSERT INTO news (
                channel_id, 
                channel_title,
                data, 
                views,
                published_at)
                 VALUES (

                :channel_id, 
                :channel_title, 
                :data, 
                :views,
                :published_at
                );""")

            await session.execute(query, params=to_insert)
            await session.commit()

    @staticmethod
    async def save_after_analysis_123123123(to_insert: dict) -> None:
        pass

    @staticmethod
    async def get_daily_news_data_for_analysis() -> typing.Any:
        async with AsyncSessionLocal() as session:
            start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_of_day = int((start_of_day.timestamp()))
            # query = text(f"""SELECT * FROM news WHERE published_at > {start_of_day};""")
            query = text("""SELECT channel_title, data FROM news;""")  # TODO: use this for debug
            # query = text("""
            # SELECT COALESCE(SUM(LENGTH(elem)), 0)
            # FROM news, unnest(data) AS elem;
            # """)  # just for analyze
            result = await session.execute(query)
            return result.fetchall()


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
                ) ON CONFLICT DO NOTING;""")

            await session.execute(query, params=to_insert)
            await session.commit()
