__all__ = ("router",)

from aiogram import Router

from core.handlers.info_handlers import router as info_router
from core.handlers.quiz_handlers import router as quiz_router
from core.handlers.rating_handlers import router as rating_router
from core.handlers.start_handlers import router as start_router

router = Router(name=__name__)

router.include_routers(rating_router, info_router, quiz_router, start_router)
