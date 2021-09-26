import carts
from typing import List
import datetime


def get_week(date) -> int:
    return datetime.date(date.year, date.month, date.day).isocalendar()[1]


class User:
    def __init__(self, user_id: int, name: str, carts: List[carts.Cart]):
        self.id = user_id
        self.name = name
        self.carts = carts
        self.friends = []

    def add_friend(self, friend):
        self.friends.append(friend)

    def add_cart(self, cart: carts.Cart):
        self.carts.append(cart)

    def score(self) -> int:
        if len(self.carts) == 0:
            return 0

        score = sum(cart.score_sum()[0] for cart in self.carts)
        num = sum(cart.score_sum()[1] for cart in self.carts)

        return round(score / num, 1)

    def weekly_score(self, n: int, current_week: int):
        """returns a list of the last `n` total weekly scores, from `current_week` backwards"""

        carts_in_week = {}
        for cart in self.carts:
            week = get_week(cart.date)
            if carts_in_week.get(week) is None:
                carts_in_week[week] = []
            carts_in_week[week].append(cart)

        avg_scores_in_week = {}
        for week, carts in carts_in_week.items():
            avg_scores_in_week[week] = sum([cart.score() for cart in carts]) / len(carts)

        weekly_scores = [
            avg_scores_in_week[week] if avg_scores_in_week.get(week) is not None else None
            for week in range(current_week - n + 1, current_week + 1)
        ]

        return weekly_scores

    def abs_score_last_5_weeks(self):
        return round(sum(self.weekly_score(5, get_week(self.carts[-1].date))), 3)

    def avg_score_last_5_weeks(self):
        return round(self.abs_score_last_5_weeks()/5, 3)
