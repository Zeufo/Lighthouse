from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from database import close_db

# /help and /github
router = Router(name=__name__)


@router.startup()
async def start() -> None:
    pass


# use queues. because we dont need to loose data. its not THAT matter for be sure data is safe, but still
@router.shutdown()
async def stop() -> None:
    await close_db()
    logger.info("Database closed")
