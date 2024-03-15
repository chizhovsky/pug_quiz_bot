from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.utils.bot_messages import greeting_text

router = Router(name=__name__)


@router.message(Command("info"))
async def get_info(message: Message):
    await message.answer(greeting_text)
