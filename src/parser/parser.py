import abc
import typing

import telethon
from telethon import TelegramClient, events

from config import API_HASH, API_ID


class Parser(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def parse() -> typing.Any:
        pass


class TelethonParser(Parser):
    @staticmethod
    async def parse() -> typing.Any:
        try:
            pass
        except Exception as e:
            pass
