from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="quiz", description="Играть"),
        BotCommand(command="info", description="О викторине"),
        BotCommand(command="rating", description="Таблица лидеров"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
