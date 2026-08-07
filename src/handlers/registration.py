from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.registration_service import UserService

# /help and /github
router = Router(name=__name__)


@router.message(Command("agree", ignore_case=True))
async def register(message: Message):
    await UserService.registrate(message)
    await message.answer('Зарегистрировано!')
