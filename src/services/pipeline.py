import asyncio
import time

from loguru import logger
from telethon import TelegramClient

from ai import WorkerAI
from config import CHANNELS, queue
from database import NewsCRUD
from parser import TelethonParser
from services.format_service import TelethonCleaner


async def full_news_cycle(channel: str, client: TelegramClient) -> None:
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
        await NewsCRUD.save_after_analysis(to_insert)
        logger.debug(f"news saved for {channel} with {views} views in total")

    except Exception as e:
        logger.exception("Error in processing full_news_cycle")


class Pipeline:
    @staticmethod
    async def process_news_and_save(client: TelegramClient) -> None:
        # for channel in CHANNELS:
        channel = CHANNELS[2]
        await queue.put((full_news_cycle, [channel, client], {}))

        await queue.join()
