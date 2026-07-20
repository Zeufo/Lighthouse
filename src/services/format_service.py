import abc
import re
import typing

from loguru import logger
from telethon.helpers import add_surrogate

from ai import WorkerAI

table = str.maketrans("", "", ",./*-")


async def is_obvious_ad(text: str) -> bool:
    AD_PATTERN = re.compile(
        r"(?:^|\s)(?:https?:/{0,2}|www\.)\S+",
        re.IGNORECASE,
    )
    if AD_PATTERN.search(text):
        return True
    return False


class Cleaner(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def clean(*args, **kwargs) -> typing.Any:
        pass


class TelethonCleaner(Cleaner):
    @staticmethod
    async def clean(text: list[str]) -> typing.Any:
        write_idx = 0
        for read_idx in range(len(text)):
            if not await is_obvious_ad(text[read_idx]):
                text[write_idx] = text[read_idx]
                write_idx += 1

        del text[write_idx:]

        # some issue with AI_API... so fake it until we fix it:
        # ai_response = await WorkerAI.is_has_ad(text)
        ai_response = [
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
            "NO",
        ]

        if ai_response is None:
            return

        write_idx = 0
        for idx, answer in enumerate(ai_response):
            if answer == "NO":
                text[write_idx] = text[idx]
                write_idx += 1

        logger.debug(f"text is {text}")
        return text
