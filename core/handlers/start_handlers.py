from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.keyboards.quiz_keyboards import start_keyboard
from core.utils.bot_messages import greeting_text

router = Router(name=__name__)


@router.message(CommandStart)
async def start_message(message: Message):
    await message.answer(
        greeting_text, parse_mode="HTML", reply_markup=start_keyboard()
    )
