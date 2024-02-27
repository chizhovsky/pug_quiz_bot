import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher

from config import token
from core.database.db_connect import connect_to_postgres
from core.middlewares.dbmiddleware import DBSession
from core.routers import router as main_router
from core.utils.start_bot import start


async def main():
    log_handler = RotatingFileHandler(filename="quiz.log", maxBytes=500000)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s "
        "(%(filename)s).%(funcName)s(%(lineno)d) %(message)s",
        datefmt="%d-%m-%Y %H:%M",
        handlers=[log_handler],
    )
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.update.middleware.register(DBSession(await connect_to_postgres()))
    bot = Bot(token=token, parse_mode="HTML")
    await start(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
