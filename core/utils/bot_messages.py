from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from emoji import emojize

from config import questions_count
from core.utils.math_operations import calculate_score_sum

emoji_dict = {
    "one": emojize(":one:", language="alias"),
    "two": emojize(":two:", language="alias"),
    "three": emojize(":three:", language="alias"),
    "four": emojize(":four:", language="alias"),
    "five": emojize(":five:", language="alias"),
    "six": emojize(":six:", language="alias"),
    "globe": emojize(":globe_showing_Europe-Africa:", language="alias"),
    "thought": emojize(":thought_balloon:", language="alias"),
}
emoji_numbers = list(emoji_dict.values())[:6]


def generate_data_user(context_data):
    data_user = ""
    for i in range(questions_count):
        emoji = emoji_numbers[i]
        answer_key = f"answer_{i}"
        score_key = f"score_{i}"
        answer = context_data.get(answer_key, "")
        score = context_data.get(score_key, 0)
        data_user += f"{emoji} {answer}\nБаллы: <b>{score}</b>\n\n"
    score_sum = calculate_score_sum(context_data)
    data_user += f"<b>Сумма баллов: {score_sum}</b>"
    return data_user, score_sum


async def set_reaction(bot, chat_id, message_id, emoji):
    reaction = ReactionTypeEmoji(type="emoji", emoji=emoji)
    await bot.set_message_reaction(chat_id, message_id, reaction=[reaction])
