import asyncio

from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, TEST_LINK
from utils import setup_logger

# TODO: make list of channels


async def attempt() -> None:
    async with TelegramClient("news_parser", API_ID, API_HASH) as client:  # type:ignore
        logger.info("Client ready")

        async for message in client.iter_messages(TEST_LINK, limit=10):
            if not message.text:
                continue

            entity = await client.get_entity(TEST_LINK)

            logger.debug(f"entity is {entity}")
            text = message.text
            table = str.maketrans("", "", ",./*-")

            logger.info("-" * 50)
            logger.info(f"📅 Дата: {message.date}")
            logger.info(f"🆔 ID сообщения: {message.id}")
            logger.info(f"👁 Просмотры: {message.views if message.views else 0}")
            logger.info(f"📝 Текст новости:\n{text.translate(table)}")

            await asyncio.sleep(1)


async def main() -> None:
    setup_logger()
    await attempt()


try:
    asyncio.run(main())

except KeyboardInterrupt:
    logger.critical("Keyboard Interrupt!")
