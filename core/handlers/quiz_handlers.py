import random
import time

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils import markdown

from config import questions_count
from core.database.get_db_data import Request, get_random_questions
from core.keyboards.quiz_keyboards import (
    category_keyboard,
    quiz_keyboard,
    restart_quiz,
)
from core.utils.bot_messages import (
    emoji_numbers,
    generate_data_user,
    set_reaction,
)
from core.utils.math_operations import calculate_score
from core.utils.states_form import QuizForm

router = Router(name=__name__)

quiz_buttons = [[] for _ in range(questions_count)]
correct_answers = [""] * questions_count
question_text = [""] * questions_count
image_urls = [""] * questions_count
quiz_forms = [
    QuizForm.SECOND_QUESTION,
    QuizForm.THIRD_QUESTION,
    QuizForm.FOURTH_QUESTION,
    QuizForm.FIFTH_QUESTION,
    QuizForm.SIXTH_QUESTION,
]


async def process_questions(random_questions):
    for i in range(questions_count):
        question = random_questions[i]
        answers = [
            question["correct_answer"],
            question["answer1"],
            question["answer2"],
            question["answer3"],
        ]
        random.shuffle(answers)
        quiz_buttons[i] = answers
        correct_answers[i] = question["correct_answer"]
        question_text[i] = question["question_text"]
        image_urls[i] = question["image_url"]
    return quiz_buttons, correct_answers, question_text, image_urls


@router.callback_query(lambda c: c.data == "start_quiz")
async def start_quiz(callback_query: CallbackQuery, state: FSMContext):
    await choose_category(callback_query.message, state)


@router.message(Command("quiz"))
async def choose_category(message: Message, state: FSMContext):
    await message.answer(
        text="Выбери категорию:",
        reply_markup=category_keyboard(),
    )
    await state.set_state(QuizForm.CHOOSE_CATEGORY)


@router.callback_query(QuizForm.CHOOSE_CATEGORY)
async def process_category(callback_query: CallbackQuery, state: FSMContext):
    selected_category = callback_query.data
    await state.update_data(category=selected_category)
    await state.set_state(QuizForm.START_QUIZ)
    await get_quiz(callback_query.message, state, callback_query.bot)


@router.message(QuizForm.START_QUIZ)
async def get_quiz(message: Message, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    global quiz_buttons, correct_answers, question_text, image_urls
    random_questions = await get_random_questions(context_data.get("category"))
    quiz_buttons, correct_answers, question_text, image_urls = (
        await process_questions(random_questions)
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Начинаем викторину ⚡️",
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{emoji_numbers[0]}{markdown.hide_link(image_urls[0])}",
        parse_mode=ParseMode.HTML,
    )
    await state.update_data(start_time_0=time.time())
    await message.answer(
        text=question_text[0],
        reply_markup=quiz_keyboard(quiz_buttons[0]),
    )
    await state.set_state(QuizForm.SECOND_QUESTION)


async def handle_question(
    message: Message,
    state: FSMContext,
    bot: Bot,
    correct_answer: str,
    emoji: str,
    image_url: str,
    next_question_text: str,
    next_question_buttons: list[str],
    answer_key: str,
    start_time_key: str,
    end_time_key: str,
    score_key: str,
    next_question_state: str,
):
    await state.update_data(
        **{answer_key: message.text, end_time_key: time.time()}
    )
    context_data = await state.get_data()
    diff_time = context_data.get(end_time_key) - context_data.get(
        start_time_key
    )
    if context_data.get(answer_key) == correct_answer:
        await state.update_data(
            **{
                answer_key: f"<b>{message.text}</b> ✅",
                score_key: calculate_score(diff_time),
            }
        )
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        await state.update_data(
            **{
                answer_key: message.text
                + f" ❌\nПравильный ответ: <b>{correct_answer}</b>"
            },
            **{score_key: 0},
        )
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{emoji}{markdown.hide_link(image_url)}",
        parse_mode=ParseMode.HTML,
    )
    await state.update_data(
        **{f"start_time_{int(start_time_key[-1]) + 1}": time.time()}
    )
    await message.answer(
        text=next_question_text,
        reply_markup=quiz_keyboard(next_question_buttons),
    )
    await state.set_state(next_question_state)


for index, question_number in enumerate(quiz_forms):

    @router.message(question_number)
    async def get_question(
        message: Message, state: FSMContext, bot: Bot, idx=index
    ):
        await handle_question(
            message,
            state,
            bot,
            correct_answers[idx],
            emoji_numbers[idx + 1],
            image_urls[idx + 1],
            question_text[idx + 1],
            quiz_buttons[idx + 1],
            f"answer_{idx}",
            f"start_time_{idx}",
            f"end_time_{idx}",
            f"score_{idx}",
            QuizForm.RESULT if idx == 4 else quiz_forms[idx + 1],
        )


@router.message(QuizForm.RESULT)
async def get_quiz_result(
    message: Message, state: FSMContext, bot: Bot, request: Request
):
    await state.update_data(answer_5=message.text, end_time_5=time.time())
    context_data = await state.get_data()
    correct_answer = correct_answers[5]
    diff_time_5 = context_data.get("end_time_5") - context_data.get(
        "start_time_5"
    )
    if context_data.get("answer_5") == correct_answer:
        context_data = await state.update_data(
            answer_5=f"<b>{message.text}</b> ✅",
            score_5=calculate_score(diff_time_5),
        )
        await set_reaction(bot, message.chat.id, message.message_id, "👍")
    else:
        context_data = await state.update_data(
            answer_5=message.text
            + f" ❌\nПравильный ответ: <b>{correct_answer}</b>",
            score_5=0,
        )
        await set_reaction(bot, message.chat.id, message.message_id, "💔")
    data_user, points = generate_data_user(context_data)
    await message.answer(
        text=f"{data_user}", reply_markup=ReplyKeyboardRemove()
    )
    await request.add_user_data(
        message.from_user.id,
        f"{message.from_user.first_name} {message.from_user.last_name}",
        points,
        context_data.get("category"),
    )
    await state.clear()
    await message.answer(text="Сыграть ещё раз?", reply_markup=restart_quiz())
