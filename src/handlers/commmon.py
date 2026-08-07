from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import text
from sqlalchemy.orm import mapped_as_dataclass

from config import ADMIN_ID
from database import AsyncSessionLocal

# /help and /github
router = Router(name=__name__)


@router.message(Command("help", ignore_case=True))
@router.message(CommandStart())
@router.message(Command("начать", ignore_case=True))
@router.message(F.text.replace(" ", "").upper().in_({"СТАРТ", "НАЧАТЬ"}))
async def say_hello(message: Message) -> None:
    await message.answer(
        """Бот сделан с целью получения доступной сводки по новостям за прошедший день.
ежедневно в 19:30 часов по МСК.\n
Вся информация береться из доступных источников.
Используйте /agree чтобы подписаться на расслыку или /commands для списка комманд.
        """
    )


@router.message(Command("info", ignore_case=True))
@router.message(Command("about", ignore_case=True))
async def info(message: Message) -> None:
    await message.answer(
        """Разрботчик ...
Ссылка на GitHub: ...
p.s. Потом как-нибудь
        """
    )


@router.message(Command("commands", ignore_case=True))
async def commands(message: Message) -> None:
    await message.answer(
        """/start начать
/commands список команд
/agree подписаться на расслыку 
/digest последняя акутальная сводка
        """
    )


@router.message(Command("admin", ignore_case=True))
async def admnin(message: Message) -> None:
    if str(message.chat.id) != ADMIN_ID:
        await message.answer("Not you..")

    else:
        async with AsyncSessionLocal() as session:
            query = text("SELECT COUNT(*) FROM users")
            result = await session.execute(query)
            result = result.scalar()
            await message.answer(f"total users... {result}")
