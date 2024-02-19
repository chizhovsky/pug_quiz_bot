from aiogram.utils.keyboard import ReplyKeyboardBuilder


def quiz_keyboard(quiz_buttons):
    keyboard_builder = ReplyKeyboardBuilder()
    for i in range(0, 4):
        keyboard_builder.button(text=quiz_buttons[i])
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True, one_time_keyboard=True
    )
