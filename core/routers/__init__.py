__all__ = ("router",)

from aiogram import Router

from core.handlers.quiz_form import router as quizform_router
from core.utils.start_bot import router as startbot_router

router = Router(name=__name__)

router.include_routers(
    quizform_router,
    startbot_router,
)
