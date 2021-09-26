import users
from typing import Dict


def get_timeline(user: users.User):

    carts = user.carts
    scores = {
        cart: cart.score()
        for cart in carts
    }

    current_week = users.get_week(carts[-1].date) if len(carts) > 0 else 0  # get_week(datetime.datetime.today())

    weekly_scores = user.weekly_score(5, current_week)

    friends_scores = {
        friend.name: friend.weekly_score(5, current_week)
        for friend in user.friends
    }

    ranking_data_dict = {
        friend.name: sum(filter(None, friends_scores[friend.name]))
        for friend in user.friends
    }
    ranking_data_dict_sorted = {k: v for k, v in sorted(ranking_data_dict.items(), key=lambda item: item[1])}

    return {
        'user_id': user.id,
        'current_week': current_week,
        # 'total_score': total_score,
        # 'avg_score': avg_score,
        'weekly_scores': weekly_scores,
        'friends_scores': friends_scores,
        'ranking': ranking_data_dict_sorted,
    }
