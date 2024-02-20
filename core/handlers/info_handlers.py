from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)


@router.message(Command("info"))
async def get_info(message: Message):
    await message.answer("Здесь будет информация")
