from aiogram import F, Router
from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated, Message
from loguru import logger

from services.registration_service import UserService

# /help and /github
router = Router(name=__name__)


@router.message(Command("agree", ignore_case=True))
async def register(message: Message):
    await UserService.registrate(message)
    await message.answer("Зарегистрировано!")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    user_id = int(event.from_user.id)
    await UserService.delete_user(user_id)
    logger.debug(f"user {user_id} was deleted")
