import abc
import asyncio
import re
import typing

from loguru import logger
from telethon.helpers import add_surrogate

from ai import WorkerAI

table = str.maketrans("", "", ",./*-")


async def is_obvious_ad(text: str) -> bool:
    AD_PATTERN = re.compile(
        r"(?:https?://|www\.|t\.me/|vk\.com/|youtube\.com/|youtu\.be/| \w\-+\.\w{2,}/)\S+",
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

        logger.debug(f"text is {text}")
        return text


CATEGORY_TITLES = {
    "politics": "🏛 Политика",
    "economy": "💰 Экономика",
    "technology": "💻 Технологии",
    "society": "⚖️ Общество",
    "crypto_fintech": "🪙 Крипто и финтех",
    "emergencies": "🚨 Происшествия",
    "culture_lifestyle": "🎭 Культура",
    "ecology": "🌿 Экология",
}

TELEGRAM_LIMIT = 4096


async def format_digest(data: dict) -> list[str]:
    """
    Принимает словарь с ключом "clusters" (результат анализа ИИ),
    возвращает список готовых сообщений для отправки в Telegram,
    каждое не длиннее 4096 символов.
    """
    clusters = data.get("clusters", [])
    if not clusters:
        return ["Сегодня значимых новостей не найдено."]

    grouped: dict[str, list[dict]] = {}
    for item in clusters:
        category = item.get("category", "other")
        grouped.setdefault(category, []).append(item)

    messages: list[str] = []
    current_message = "📰 <b>Новости за сегодня</b>\n"

    for category, items in grouped.items():
        title = CATEGORY_TITLES.get(category, category.capitalize())
        block = f"\n<b>{title}</b>\n"

        for item in items:
            news_title = item.get("title", "")
            summary = item.get("summary", "")
            fact_quality = item.get("fact_quality", 0)
            channels = item.get("channels", [])

            reliability = "✅" if fact_quality >= 4 else "⚠️" if fact_quality >= 2 else "❓"
            sources = len(channels)

            if sources == 0:
                sources = "Не указаны"

            entry = f"\n{reliability} <b>{news_title}</b>\n{summary}\n<i>Источники: {sources}</i>\n"

            if len(current_message) + len(block) + len(entry) > TELEGRAM_LIMIT:
                messages.append(current_message.strip())
                current_message = f"<b>{title}</b> (продолжение)\n"
                block = ""

            current_message += block + entry
            block = ""

        await asyncio.sleep(0)

    if current_message.strip():
        messages.append(current_message.strip())

    return messages
