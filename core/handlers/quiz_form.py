from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.quiz_keyboard import quiz_keyboard
from core.utils.set_message_reaction import set_reaction
from core.utils.states_form import QuizForm

router = Router(name=__name__)

quiz_buttons = [
    ["Россия", "Испания", "Италия", "Германия"],
    ["Япония", "Китай", "Индия", "Южная Корея"],
    ["Великобритания", "США", "Австралия", "Канада"],
    ["Италия", "Германия", "Испания", "Франция"],
    ["Канада", "Мальдивы", "Новая Зеландия", "Австралия"],
    ["Таджикистан", "Узбекистан", "Кыргызстан", "Туркменистан"],
]
correct_answers = {0: "Италия", 1: "Япония", 2: "США",
                   3: "Испания", 4: "Австралия", 5: "Таджикистан"}


@router.message(Command("quiz"))
async def get_quiz(message: Message, state: FSMContext):
    await message.answer(
        f"{message.from_user.first_name}, начинаем викторину.\n"
        f"Вопрос 1:\nСтолицей какой страны является Рим?",
        reply_markup=quiz_keyboard(quiz_buttons[0]),
    )
    await state.set_state(QuizForm.SECOND_QUESTION)


@router.message(QuizForm.SECOND_QUESTION)
async def get_second_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer0=message.text)
    context_data = await state.get_data()
    if context_data.get("answer0") == correct_answers[0]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        "Вопрос 2:\nСтолицей какой страны является Токио?",
        reply_markup=quiz_keyboard(quiz_buttons[1]),
    )
    await state.set_state(QuizForm.THIRD_QUESTION)


@router.message(QuizForm.THIRD_QUESTION)
async def get_third_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer1=message.text)
    context_data = await state.get_data()
    if context_data.get("answer1") == correct_answers[1]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        "Вопрос 3:\nСтолицей какой страны является Вашингтон?",
        reply_markup=quiz_keyboard(quiz_buttons[2]),
    )
    await state.set_state(QuizForm.FOURTH_QUESTION)


@router.message(QuizForm.FOURTH_QUESTION)
async def get_fourth_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer2=message.text)
    context_data = await state.get_data()
    if context_data.get("answer2") == correct_answers[2]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        "Вопрос 4:\nСтолицей какой страны является Мадрид?",
        reply_markup=quiz_keyboard(quiz_buttons[3]),
    )
    await state.set_state(QuizForm.FIFTH_QUESTION)


@router.message(QuizForm.FIFTH_QUESTION)
async def get_fifth_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer3=message.text)
    context_data = await state.get_data()
    if context_data.get("answer3") == correct_answers[3]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        "Вопрос 5:\nСтолицей какой страны является Канберра?",
        reply_markup=quiz_keyboard(quiz_buttons[4]),
    )
    await state.set_state(QuizForm.SIXTH_QUESTION)


@router.message(QuizForm.SIXTH_QUESTION)
async def get_sixth_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer4=message.text)
    context_data = await state.get_data()
    if context_data.get("answer4") == correct_answers[4]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        "Вопрос 6:\nСтолицей какой страны является Душанбе?",
        reply_markup=quiz_keyboard(quiz_buttons[5]),
    )
    await state.set_state(QuizForm.RESULT)


@router.message(QuizForm.RESULT)
async def get_quiz_result(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer5=message.text)
    context_data = await state.get_data()
    if context_data.get("answer5") == correct_answers[5]:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    data_user = (
        f"Ответ 1: {context_data.get('answer0')}\r\n"
        f"Ответ 2: {context_data.get('answer1')}\r\n"
        f"Ответ 3: {context_data.get('answer2')}\r\n"
        f"Ответ 4: {context_data.get('answer3')}\r\n"
        f"Ответ 5: {context_data.get('answer4')}\r\n"
        f"Ответ 6: {context_data.get('answer5')}"
    )
    await message.answer(data_user)
    await state.clear()





"""async def handle_question_answer(message: Message, state: FSMContext, bot: Bot, answer_key: str, correct_answer: str, next_question_text: str, next_question_buttons: list[str]):
    await state.update_data(**{answer_key: message.text})
    context_data = await state.get_data()
    if context_data.get(answer_key) == correct_answer:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        next_question_text,
        reply_markup=quiz_keyboard(next_question_buttons),
    )
    await state.set_state(QuizForm.THIRD_QUESTION if answer_key == "answer0" else QuizForm.RESULT)


@router.message(QuizForm.SECOND_QUESTION)
async def get_second_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question_answer(
        message, state, bot, "answer0", correct_answers[0],
        "Вопрос 2:\nСтолицей какой страны является Токио?",
        quiz_buttons[1]
    )


@router.message(QuizForm.THIRD_QUESTION)
async def get_third_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question_answer(
        message, state, bot, "answer1", correct_answers[1],
        "Вопрос 3:\nСтолицей какой страны является Вашингтон?",
        quiz_buttons[2]
    )"""

