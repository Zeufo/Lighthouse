import asyncio
import json
import time
import typing
from pathlib import Path

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


# TODO: ACtuall all down is not for news service
async def format_data_for_ai(raw: list[tuple[str, list]]) -> list:
    formatted = [{"channel": ch, "data": d} for ch, d in raw]
    return formatted


CACHE_FILE = Path("cache/daily_analyze.json")


async def analyze_daily_data() -> typing.Any:
    if CACHE_FILE.exists():
        logger.debug("loading from cache")
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    info = await NewsCRUD.get_daily_news_data_for_analysis()
    info = await format_data_for_ai(info)
    logger.debug("data has been formatted for ai")
    response = await WorkerAI.analyze_daily_data(info)

    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
