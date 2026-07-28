import asyncio
import json
import time
import typing
from datetime import datetime, timezone
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
        start = time.time()
        if not client.is_connected():
            await client.connect()

        last_parse_session = await NewsCRUD.get_last_parse_session_time()

        if last_parse_session is None or last_parse_session[0] is None:
            last_parse_session = datetime.now(timezone.utc).date()  # today
        else:
            last_parse_session = datetime.fromtimestamp(
                last_parse_session[0], tz=timezone.utc
            ).date()

        parsed = await TelethonParser.parse_today_news(channel, last_parse_session, client)
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
        logger.debug(f"collect news cycle took {int(time.time() - start)} seconds")

    except Exception as e:
        logger.exception("Error in processing full_news_cycle")


async def format_data_for_ai(raw: list[tuple[str, list]]) -> list:
    formatted = [{"channel": ch, "data": d} for ch, d in raw]
    return formatted


CACHE_FILE = Path("cache/daily_analyze.json")


async def analyze_daily_data() -> typing.Any:
    if CACHE_FILE.exists():
        logger.debug("loading from cache")
        with open(CACHE_FILE, "r") as f:
            response = json.load(f)

            logger.debug(response)
            await NewsCRUD.save_after_analysis(response)

    info = await NewsCRUD.get_daily_news_data_for_analysis()
    info = await format_data_for_ai(info)
    logger.debug("data has been formatted for ai")
    response = await WorkerAI.analyze_daily_data(info)
    await NewsCRUD.save_after_analysis(response)

    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
