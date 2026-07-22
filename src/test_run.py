import asyncio

from database import NewsCRUD


async def try_() -> None:
    res = await NewsCRUD.get_daily_news_data_for_analysis()
    print(res)
    # 22 jule. from all news channel total 229046 symbols


if __name__ == "__main__":
    asyncio.run(try_())
