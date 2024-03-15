from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from core.utils.bot_messages import emoji_dict


def quiz_keyboard(quiz_buttons):
    keyboard_builder = ReplyKeyboardBuilder()
    for i in range(0, 4):
        keyboard_builder.button(text=quiz_buttons[i])
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True, one_time_keyboard=True
    )


def category_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text=f"Общие знания {emoji_dict['thought']}", callback_data="1"
    )
    keyboard_builder.button(
        text=f"География {emoji_dict['globe']}", callback_data="2"
    )
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(
        resize_keyboard=True, one_time_keyboard=True
    )


def start_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Начать игру", callback_data="start_quiz")
    return keyboard_builder.as_markup(resize_keyboard=True)


def restart_quiz():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Играть! ⚡️", callback_data="start_quiz")
    return keyboard_builder.as_markup(resize_keyboard=True)
