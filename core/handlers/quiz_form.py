from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import (
    emoji_five,
    emoji_four,
    emoji_one,
    emoji_six,
    emoji_three,
    emoji_two,
)
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
correct_answers = {
    0: "Италия",
    1: "Япония",
    2: "США",
    3: "Испания",
    4: "Австралия",
    5: "Таджикистан",
}


@router.message(Command("quiz"))
async def get_quiz(message: Message, state: FSMContext):
    await message.answer(
        f"{message.from_user.first_name}, начинаем викторину."
    )
    await message.answer(
        f"{emoji_one} Столицей какой страны является Рим?",
        reply_markup=quiz_keyboard(quiz_buttons[0]),
    )
    await state.set_state(QuizForm.SECOND_QUESTION)


async def handle_question(
    message: Message,
    state: FSMContext,
    bot: Bot,
    answer_key: str,
    correct_answer: str,
    next_question_text: str,
    next_question_buttons: list[str],
    emoji: str,
):
    await state.update_data(**{answer_key: message.text})
    context_data = await state.get_data()
    if context_data.get(answer_key) == correct_answer:
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await message.answer(
        f"{emoji} {next_question_text}",
        reply_markup=quiz_keyboard(next_question_buttons),
    )
    next_question_state = QuizForm.NEXT_QUESTION_MAPPING.get(answer_key)
    if next_question_state:
        await state.set_state(next_question_state)
    else:
        await state.set_state(QuizForm.RESULT)


@router.message(QuizForm.SECOND_QUESTION)
async def get_second_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        "answer0",
        correct_answers[0],
        "Столицей какой страны является Токио?",
        quiz_buttons[1],
        emoji_two,
    )


@router.message(QuizForm.THIRD_QUESTION)
async def get_third_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        "answer1",
        correct_answers[1],
        "Столицей какой страны является Вашингтон?",
        quiz_buttons[2],
        emoji_three,
    )


@router.message(QuizForm.FOURTH_QUESTION)
async def get_fourth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        "answer2",
        correct_answers[2],
        "Столицей какой страны является Мадрид?",
        quiz_buttons[3],
        emoji_four,
    )


@router.message(QuizForm.FIFTH_QUESTION)
async def get_fifth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        "answer3",
        correct_answers[3],
        "Столицей какой страны является Канберра?",
        quiz_buttons[4],
        emoji_five,
    )


@router.message(QuizForm.SIXTH_QUESTION)
async def get_sixth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        "answer4",
        correct_answers[4],
        "Столицей какой страны является Душанбе?",
        quiz_buttons[5],
        emoji_six,
    )


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
