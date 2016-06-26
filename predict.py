"""
Get predictions by ids of user's news
"""


def predict(first_id=None, second_id=None, third_id=None):
    """
    Get news predictions. If one of ids isn't specified,
    so replace it to most popular articles. If none of ids
    is specified, get most popular news.
    :param first_id: MongoDB id of first article
    :param second_id:
    :param third_id:
    :return: [{'id': '', 'url': '', 'title': ''}, ...]
    """
    pass
