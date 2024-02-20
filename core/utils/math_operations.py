import math


def calculate_score(time_seconds):
    time_to_half = math.floor(time_seconds * 2 + 0.5) / 2
    score = 20 - int(time_to_half / 0.5)
    return score


def calculate_score_sum(context_data):
    score_sum = sum(context_data.get(f"score_{i}", 0) for i in range(6))
    return score_sum
