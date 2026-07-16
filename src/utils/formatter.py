import abc
import re
import typing

from loguru import logger
from telethon.helpers import add_surrogate

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
        try:
            skipped = []
            clean_post = []

            for post in text:
                if await is_obvious_ad(post):
                    skipped.append(post)
                else:
                    clean_post.append(post.translate(table))

            # use this if we notice that no channels use links at news. one line, bro
            # clean_post = [post.translate(table) for post in text if not await is_obvious_ad(post)]
            #
            return clean_post
        except Exception as e:
            pass
