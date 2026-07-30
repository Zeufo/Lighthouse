import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from config import API_HASH, API_ID, BOT_TOKEN, CHANNELS, TEST_LINK

BOT = Bot(token=BOT_TOKEN)  # type: ignore
