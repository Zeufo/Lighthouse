import asyncio
import json
from pathlib import Path

from loguru import logger

from database import NewsCRUD

CACHE_FILE = Path("cache/daily_analyze.json")


async def try_() -> None:
    if CACHE_FILE.exists():
        logger.debug("loading from cache")
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    CACHE_FILE.parent.mkdir(exist_ok=True)
    response = {"data": "info"}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=2)

    # res = await NewsCRUD.get_daily_news_data_for_analysis()
    # print(res)
    # 22 jule. from all news channel total 229046 symbols


if __name__ == "__main__":
    asyncio.run(try_())
