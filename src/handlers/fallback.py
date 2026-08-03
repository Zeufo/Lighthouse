from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# /help and /github
router = Router(name=__name__)


@router.message()
async def commands(message: Message) -> None:
    await message.answer(
        """/start начать
/commands список команд
/agree подписаться на расслыку 
/digest последняя акутальная сводка
        """
    )
