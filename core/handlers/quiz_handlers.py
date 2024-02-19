from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

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
image_urls = {
    0: "https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
    1: "https://images.unsplash.com/photo-1513407030348-c983a97b98d8?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
    2: "https://images.unsplash.com/photo-1552337125-0c43e12efec0?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
    3: "https://images.unsplash.com/photo-1543783207-ec64e4d95325?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
    4: "https://images.unsplash.com/photo-1611231731916-826fe315c533?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
    5: "https://images.unsplash.com/photo-1707663154646-06390356b683?q=80&w=480&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # noqa
}


@router.message(Command("quiz"))
async def get_quiz(message: Message, state: FSMContext):
    await message.answer(
        f"{message.from_user.first_name}, начинаем викторину."
    )
    await message.answer(
        text=f"{emoji_one}{markdown.hide_link(image_urls[0])}",
        parse_mode=ParseMode.HTML,
    )
    await message.answer(
        text="Столицей какой страны является Рим?",
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
    url: str,
):
    await state.update_data(**{answer_key: message.text})
    context_data = await state.get_data()
    if context_data.get(answer_key) == correct_answer:
        await state.update_data(**{answer_key: f"<b>{message.text}</b> ✅"})
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await state.update_data(
            **{
                answer_key: message.text
                + f" ❌\nПравильный ответ: <b>{correct_answer}</b>"
            }
        )
        await set_reaction(bot, message.chat.id, message.message_id, "💔")

    await message.answer(
        text=f"{emoji}{markdown.hide_link(url)}", parse_mode=ParseMode.HTML
    )
    await message.answer(
        text=f"{next_question_text}",
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
        image_urls[1],
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
        image_urls[2],
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
        image_urls[3],
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
        image_urls[4],
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
        image_urls[5],
    )


@router.message(QuizForm.RESULT)
async def get_quiz_result(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(answer5=message.text)
    context_data = await state.get_data()
    correct_answer = correct_answers[5]
    if context_data.get("answer5") == correct_answer:
        context_data = await state.update_data(
            answer5=f"<b>{message.text}</b> ✅"
        )
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        context_data = await state.update_data(
            answer5=message.text
            + f" ❌\nПравильный ответ: <b>{correct_answer}</b>"
        )
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    data_user = (
        f"{emoji_one} {context_data.get('answer0')}\n\n"
        f"{emoji_two} {context_data.get('answer1')}\n\n"
        f"{emoji_three} {context_data.get('answer2')}\n\n"
        f"{emoji_four} {context_data.get('answer3')}\n\n"
        f"{emoji_five} {context_data.get('answer4')}\n\n"
        f"{emoji_six} {context_data.get('answer5')}"
    )
    await message.answer(data_user)
    await state.clear()
