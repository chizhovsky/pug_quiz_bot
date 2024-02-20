from emoji import emojize

from core.utils.math_operations import calculate_score_sum

emoji_list = [
    emojize(":one:", language="alias"),
    emojize(":two:", language="alias"),
    emojize(":three:", language="alias"),
    emojize(":four:", language="alias"),
    emojize(":five:", language="alias"),
    emojize(":six:", language="alias"),
]


def generate_data_user(context_data):
    data_user = ""
    for i in range(6):
        emoji = emoji_list[i]
        answer_key = f"answer_{i}"
        score_key = f"score_{i}"
        answer = context_data.get(answer_key, "")
        score = context_data.get(score_key, 0)
        data_user += f"{emoji} {answer}\nБаллы: <b>{score}</b>\n\n"
    score_sum = calculate_score_sum(context_data)
    data_user += f"<b>Сумма баллов: {score_sum}</b>"
    return data_user
