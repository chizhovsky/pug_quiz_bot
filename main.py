import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import token
from core.routers import router as main_router
from core.utils.start_bot import start


async def main():
    dp = Dispatcher()
    dp.include_router(main_router)
    logging.basicConfig(
        filename="quiz.log",
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s "
        "(%(filename)s).%(funcName)s(%(lineno)d) %(message)s",
        datefmt="%d-%m-%Y %H:%M",
    )
    bot = Bot(token=token, parse_mode="HTML")
    await start(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
