from aiogram.fsm.state import State, StatesGroup


class QuizForm(StatesGroup):
    START_QUIZ = State()
    SECOND_QUESTION = State()
    THIRD_QUESTION = State()
    FOURTH_QUESTION = State()
    FIFTH_QUESTION = State()
    SIXTH_QUESTION = State()
    RESULT = State()
