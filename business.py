import users
from typing import Dict

import datetime


def get_week(date: datetime.datetime) -> int:
    return datetime.date(date.year, date.month, date.day).isocalendar().week


def get_timeline(user):

    user_id = 100688    # just for dev
    # user = users[user_id]
    carts = user.carts
    scores = {
        cart: cart.score()
        for cart in carts
    }

    total_score = 0
    for cart, score in scores.items():
        total_score += cart.score()
    avg_score = (total_score / len(scores)) if len(scores) > 0 else 0

    carts_in_week = {}
    for cart in carts:
        week = get_week(cart.date)
        if carts_in_week.get(week) is None:
            carts_in_week[week] = []
        carts_in_week[week].append(cart)

    avg_scores_in_week = {}
    for week, carts in carts_in_week.items():
        avg_scores_in_week[week] = sum([cart.score() for cart in carts]) / len(carts)

    current_week = get_week(datetime.datetime().today())

    weekly_scores = [
        avg_scores_in_week[week].score() if avg_scores_in_week.get(week) is not None else None
        for week in range(current_week-9, current_week+1)
    ]

    return {
        'user_id': user_id,
        'current_week': current_week,
        'total_score': total_score,
        'avg_score': avg_score,
        'weekly_scores': weekly_scores,
        'friends': {

        }
    }
