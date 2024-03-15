from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core.database.get_db_data import get_rating
from core.keyboards.quiz_keyboards import category_keyboard
from core.utils.states_form import RatingForm

router = Router(name=__name__)


@router.message(Command("rating"))
async def get_rating_message(message: Message, state: FSMContext):
    await message.answer(
        text="Топ-10 игроков в категории:",
        reply_markup=category_keyboard(),
    )
    await state.set_state(RatingForm.CHOOSE_CATEGORY)


@router.callback_query(RatingForm.CHOOSE_CATEGORY)
async def process_rating(callback_query: CallbackQuery, state: FSMContext):
    selected_category = callback_query.data
    await state.update_data(category=selected_category)
    await state.set_state(RatingForm.RATING)
    await get_rating_list(state, callback_query.message)


@router.message(RatingForm.RATING)
async def get_rating_list(state: FSMContext, message: Message):
    context_data = await state.get_data()
    selected_category = context_data.get("category")
    rating = await get_rating(selected_category)
    rating_message = ""
    place = 0
    for i in range(len(rating)):
        place += 1
        rating_message += f"{place}) <b>{rating[i][0]}</b> {rating[i][1]}\n"
    await message.answer(rating_message)
    await state.clear()
