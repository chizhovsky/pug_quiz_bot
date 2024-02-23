import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher

from config import token
from core.database.db_connect import get_db_questions
from core.routers import router as main_router
from core.utils.start_bot import start


async def main():
    await get_db_questions()
    dp = Dispatcher()
    dp.include_router(main_router)
    log_handler = RotatingFileHandler(filename="quiz.log", maxBytes=500000)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s "
        "(%(filename)s).%(funcName)s(%(lineno)d) %(message)s",
        datefmt="%d-%m-%Y %H:%M",
        handlers=[log_handler],
    )
    bot = Bot(token=token, parse_mode="HTML")
    await start(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
