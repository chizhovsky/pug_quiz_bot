import random
import time

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from config import questions_count
from core.database.db_connect import get_random_questions
from core.keyboards.quiz_keyboards import quiz_keyboard
from core.utils.bot_messages import (
    emoji_list,
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


async def process_questions(random_questions):
    for i in range(questions_count):
        question = random_questions[i]
        answers = [
            question["answer1"],
            question["answer2"],
            question["answer3"],
            question["answer4"],
        ]
        random.shuffle(answers)
        quiz_buttons[i] = answers
        correct_answers[i] = question["correct_answer"]
        question_text[i] = question["question_text"]
        image_urls[i] = question["image_url"]
    return quiz_buttons, correct_answers, question_text, image_urls


@router.message(Command("quiz"))
async def get_quiz(message: Message, state: FSMContext, bot: Bot):
    random_questions = await get_random_questions()
    quiz_buttons, correct_answers, question_text, image_urls = (
        await process_questions(random_questions)
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{message.from_user.first_name}, начинаем викторину.",
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{emoji_list[0]}{markdown.hide_link(image_urls[0])}",
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


@router.message(QuizForm.SECOND_QUESTION)
async def get_second_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        correct_answers[0],
        emoji_list[1],
        image_urls[1],
        question_text[1],
        quiz_buttons[1],
        "answer_0",
        "start_time_0",
        "end_time_0",
        "score_0",
        QuizForm.THIRD_QUESTION,
    )


@router.message(QuizForm.THIRD_QUESTION)
async def get_third_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        correct_answers[1],
        emoji_list[2],
        image_urls[2],
        question_text[2],
        quiz_buttons[2],
        "answer_1",
        "start_time_1",
        "end_time_1",
        "score_1",
        QuizForm.FOURTH_QUESTION,
    )


@router.message(QuizForm.FOURTH_QUESTION)
async def get_fourth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        correct_answers[2],
        emoji_list[3],
        image_urls[3],
        question_text[3],
        quiz_buttons[3],
        "answer_2",
        "start_time_2",
        "end_time_2",
        "score_2",
        QuizForm.FIFTH_QUESTION,
    )


@router.message(QuizForm.FIFTH_QUESTION)
async def get_fifth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        correct_answers[3],
        emoji_list[4],
        image_urls[4],
        question_text[4],
        quiz_buttons[4],
        "answer_3",
        "start_time_3",
        "end_time_3",
        "score_3",
        QuizForm.SIXTH_QUESTION,
    )


@router.message(QuizForm.SIXTH_QUESTION)
async def get_sixth_question(message: Message, state: FSMContext, bot: Bot):
    await handle_question(
        message,
        state,
        bot,
        correct_answers[4],
        emoji_list[5],
        image_urls[5],
        question_text[5],
        quiz_buttons[5],
        "answer_4",
        "start_time_4",
        "end_time_4",
        "score_4",
        QuizForm.RESULT,
    )


@router.message(QuizForm.RESULT)
async def get_quiz_result(message: Message, state: FSMContext, bot: Bot):
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
    data_user = generate_data_user(context_data)
    await message.answer(data_user)
    await state.clear()
