import abc
import asyncio
import typing

import telethon
from loguru import logger
from telethon import TelegramClient, events

from config import API_HASH, API_ID, CHANNELS, TEST_LINK


class Parser(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def parse() -> typing.Any:
        pass


class TelethonParser:
    @staticmethod
    async def parse_channels_info() -> typing.Any:
        try:
            logger.debug("into parse_channels_info")
            async with TelegramClient("news_parser_test", API_ID, API_HASH) as client:  # type:ignore
                logger.debug("Client ready")
                for channel in CHANNELS:
                    try:
                        logger.debug(f"Channel: {channel}")
                        obj = await client.get_entity(channel)
                        await asyncio.sleep(1)
                    except Exception as e:
                        logger.error(f"Error in parsing {channel}...")

            logger.debug("out of parse_channels_info")
        except Exception as e:
            logger.error("Error in parse_channels_info", e)


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
