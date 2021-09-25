import users
from typing import Dict

import datetime


def get_week(date: datetime.datetime) -> int:
    return datetime.date(date.year, date.month, date.day).isocalendar()[1]


def get_user_weeks_score(user: users.User, num_weeks: int, current_week: int):
    carts_in_week = {}
    for cart in user.carts:
        week = get_week(cart.date)
        if carts_in_week.get(week) is None:
            carts_in_week[week] = []
        carts_in_week[week].append(cart)

    avg_scores_in_week = {}
    for week, carts in carts_in_week.items():
        avg_scores_in_week[week] = sum([cart.score() for cart in carts]) / len(carts)

    weekly_scores = [
        avg_scores_in_week[week] if avg_scores_in_week.get(week) is not None else None
        for week in range(current_week - num_weeks + 1, current_week + 1)
    ]

    return weekly_scores


def get_timeline(user: users.User):

    carts = user.carts
    scores = {
        cart: cart.score()
        for cart in carts
    }

    total_score = 0
    for cart, score in scores.items():
        total_score += cart.score()
    avg_score = (total_score / len(scores)) if len(scores) > 0 else 0

    current_week = get_week(carts[-1].date) if len(carts) > 0 else 0  # get_week(datetime.datetime.today())

    weekly_scores = get_user_weeks_score(user, 5, current_week)

    friends_scores = {
        friend.name: get_user_weeks_score(friend, 5, current_week)
        for friend in user.friends
    }

    return {
        'user_id': user.id,
        'current_week': current_week,
        'total_score': total_score,
        'avg_score': avg_score,
        'weekly_scores': weekly_scores,
        'friends_scores': friends_scores,
    }
