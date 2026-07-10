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
async def say_hello(message: Message, state: FSMContext) -> None:
    pass


@router.message(Command("info", ignore_case=True))
@router.message(Command("about", ignore_case=True))
async def info(message: Message) -> None:
    await message.answer(
        """
        """
    )


@router.message(Command("commands", ignore_case=True))
async def commands(message: Message) -> None:
    await message.answer(
        """/start начать
/commands список команд
/info и /about информация о проекте
/settings настройки (не реализовано)
        """
    )
