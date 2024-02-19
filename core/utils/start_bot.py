from aiogram import Bot, Dispatcher, Router

from config import admin_chat_id
from core.utils.commands import set_commands

router = Router(name=__name__)


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_chat_id, text="Бот запущен!")


async def stop_bot(bot: Bot):
    await bot.send_message(admin_chat_id, text="Бот остановлен!")


async def start(bot: Bot, dp: Dispatcher):
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
