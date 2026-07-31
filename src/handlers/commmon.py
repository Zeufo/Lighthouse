from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# /help and /github
router = Router(name=__name__)


@router.message(Command("help", ignore_case=True))
@router.message(CommandStart())
@router.message(Command("начать", ignore_case=True))
@router.message(F.text.replace(" ", "").upper().in_({"СТАРТ", "НАЧАТЬ"}))
async def say_hello(message: Message) -> None:
    await message.answer(
        """Бот сделан с целью получения доступной сводки по новостям за прошедший день.
ежедневно в 19:00 часов по МСК.\n
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
