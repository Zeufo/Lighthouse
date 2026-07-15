import abc
import asyncio
import time
import typing
from datetime import datetime, timezone

import telethon
from loguru import logger
from telethon import TelegramClient

from config import API_HASH, API_ID, CHANNELS, queue
from utils import TelethonCleaner


class Parser(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def parse() -> typing.Any:
        pass


class TelethonParser:
    # actually there is no need in this func while creating tables when we have info parser but maybe we will use it
    # and reconstruct like a ping func
    @staticmethod
    async def parse_channels_status(client: TelegramClient) -> typing.Any:
        bad_channels = {}
        logger.debug("into parse_channels_status")
        logger.debug("Client ready")
        for channel in CHANNELS:
            try:
                logger.debug(f"Channel: {channel}...")
                channel_id = await client.get_peer_id(channel)

            except Exception as e:
                logger.warning(f"Error in getting status {channel}...")
                bad_channels[channel] = channel

            await asyncio.sleep(1)

        logger.debug("out of parse_channels_status")
        return bad_channels

    @staticmethod
    async def parse_channels_info(client: TelegramClient) -> list:
        info = []
        for channel in CHANNELS:
            try:
                channel_id = await client.get_peer_id(channel)

                await asyncio.sleep(1)
                subscribers = await client.get_participants(channel_id, limit=0)
                subscribers_count = subscribers.total
                logger.debug(f"info {channel}:{subscribers_count}")

                to_insert = {
                    "channel_id": channel_id,
                    "channel_title": channel,
                    "channel_status": True,
                    "subscribers": subscribers_count,
                    "last_parsed_at": int(time.time()),
                    "last_updated_at": int(time.time()),
                }
                info.append(to_insert)

            except Exception as e:
                logger.exception(f"Error in parsing {channel}...")
                to_insert = {
                    "channel_id": 0,
                    "channel_title": channel,
                    "channel_status": False,
                    "subscribers": 0,
                    "last_parsed_at": int(time.time()),
                    "last_updated_at": int(time.time()),
                }
                info.append(to_insert)

            await asyncio.sleep(1)

        return info

    @staticmethod
    async def parse_today_news(client: TelegramClient) -> typing.Any:  # add session type
        parsed = 0  # just for test

        today = datetime.now(timezone.utc).date()
        for channel in CHANNELS:
            text = ""
            try:
                parsed += 1
                logger.debug(f"parsing {channel}...")

                async for message in client.iter_messages(channel):
                    logger.debug("recived message!")
                    await asyncio.sleep(1)

                    text += "\n" + message.text
                    if message.date.date() != today:
                        break

            except Exception as e:
                logger.exception(f"Error in parsing {channel}...")

            if len(text) > 100:
                await queue.put((TelethonCleaner.clean, [text], {}))

            if parsed == 5:  # just for test
                await asyncio.sleep(120)
