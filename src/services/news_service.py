import asyncio
import time
import typing

from loguru import logger
from telethon import TelegramClient

from ai import WorkerAI
from config import CHANNELS, queue
from database import AsyncSessionLocal, NewsCRUD
from parser import TelethonParser
from services.format_service import TelethonCleaner


async def collect_news_cycle(channel: str, client: TelegramClient) -> None:
    try:
        if not client.is_connected():
            await client.connect()

        parsed = await TelethonParser.parse_today_news(
            channel, client
        )  # return [data, channel_id, views]
        # news = await WorkerAI.is_has_ad(news)#TODO: separate cleaner from ai opinion
        news = await TelethonCleaner.clean(parsed[0])
        channel_id = parsed[1]
        views = parsed[2]

        to_insert = {
            "channel_id": channel_id,
            "channel_title": channel,
            "data": news,
            "views": views,
            "published_at": int(time.time()),
        }
        await NewsCRUD.save_after_collect(to_insert)
        logger.debug(f"news saved for {channel} with {views} views in total")

    except Exception as e:
        logger.exception("Error in processing full_news_cycle")


async def analyze_daily_data() -> typing.Any:
    info = await NewsCRUD.get_daily_news_data_for_analysis()
