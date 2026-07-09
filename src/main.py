import asyncio

from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, CHANNELS, TEST_LINK
from utils import setup_logger

# TODO: Put it in Docker IDK


async def attempt() -> None:
    async with TelegramClient("news_parser", API_ID, API_HASH) as client:  # type:ignore
        logger.info("Client ready")
        bad_channels = 0
        good_channels = 0

        for channel in CHANNELS:
            try:
                obj = await client.get_entity(channel)
                logger.debug(f"{channel} is OK")
                good_channels += 1

            except Exception as e:
                bad_channels += 1
            finally:
                await asyncio.sleep(1)

    logger.debug(f"Bad channels: {bad_channels}")
    logger.debug(f"Good channels: {good_channels}")


async def main() -> None:
    setup_logger()
    await attempt()


try:
    asyncio.run(main())

except KeyboardInterrupt:
    logger.critical("Keyboard Interrupt!")
