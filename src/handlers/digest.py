from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from telethon.tl.types import InputGeoPointEmpty

from services.news_service import send_digest_to_users

# /help and /github
router = Router(name=__name__)


@router.message(Command("digest"))
async def need_news(message: Message) -> None:
    await send_digest_to_users(str(message.chat.id))
