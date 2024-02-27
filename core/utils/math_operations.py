import math

from config import questions_count


def calculate_score(time_seconds):
    time_to_half = math.floor(time_seconds * 2 + 0.5) / 2
    score = 20 - int(time_to_half / 0.5)
    return max(score, 1)


def calculate_score_sum(context_data):
    score_sum = sum(
        context_data.get(f"score_{i}", 0) for i in range(questions_count)
    )
    return score_sum
