from aiogram.fsm.state import State, StatesGroup


class QuizForm(StatesGroup):
    START_QUIZ = State()
    SECOND_QUESTION = State()
    THIRD_QUESTION = State()
    FOURTH_QUESTION = State()
    FIFTH_QUESTION = State()
    SIXTH_QUESTION = State()
    RESULT = State()

    NEXT_QUESTION_MAPPING = {
        "answer0": THIRD_QUESTION,
        "answer1": FOURTH_QUESTION,
        "answer2": FIFTH_QUESTION,
        "answer3": SIXTH_QUESTION,
        "answer4": RESULT,
    }
