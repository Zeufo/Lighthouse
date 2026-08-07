import abc
import time
import typing
from datetime import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import Row, insert, text
from telethon import TelegramClient
from telethon.errors import ChannelInvalidError
from telethon.tl.types import channels

from .models import AsyncSessionLocal, Base, Digest, News, engine


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
            try:
                query = insert(News).values(**to_insert)
                await session.execute(query)
                await session.commit()
            except Exception as e:
                logger.exception("Error in saving news", e)

    @staticmethod
    async def save_after_analysis(to_insert: dict) -> Row | None:
        async with AsyncSessionLocal() as session:
            date = int(time.time())
            query = insert(Digest).values(content=to_insert, date=date)
            await session.execute(query, {"to_insert": to_insert})
            await session.commit()

    @staticmethod
    async def get_last_parse_session_time() -> Optional[Row]:
        async with AsyncSessionLocal() as session:
            query = text("SELECT MAX(published_at) FROM news")
            result = await session.execute(query)
            return result.fetchone()

    @staticmethod
    async def get_daily_news_data_for_analysis() -> typing.Any:
        async with AsyncSessionLocal() as session:
            start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_of_day = int((start_of_day.timestamp()))
            query = text("""SELECT channel_title, data
            FROM news
            WHERE published_at >= COALESCE(
            (SELECT MAX(date) FROM digest),
            :fallback_time);
            """)

            result = await session.execute(query, {"fallback_time": start_of_day})
            return result.fetchall()

    @staticmethod
    async def get_digest() -> typing.Any:
        async with AsyncSessionLocal() as session:
            query = text("""SELECT content, date FROM digest ORDER By date DESC LIMIT 1;""")
            result = await session.execute(query)
            return result.fetchone()


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
                ) ON CONFLICT DO NOTHING;""")

            await session.execute(query, params=to_insert)
            await session.commit()
