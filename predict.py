"""
Get predictions by ids of user's news
"""
from models import hybrid_model

model = hybrid_model
model_init = False


def predict(first_url=None, second_url=None, third_url=None,
            tvrain_data=None, recommends_num=3):
    """
    Get news predictions. If one of ids isn't specified,
    so replace it to most popular articles. If none of ids
    is specified, get most popular news.
    :param first_url: MongoDB url of first article
    :param second_url:
    :param third_url:
    :param tvrain_data: data.data_utils.TvrainData object
    :param recommends_num: num of articles to recommend
    :return: [{'id': '', 'url': '', 'title': ''}, ...]
    """
    global model_init

    input_ids = [first_url, second_url, third_url]

    input_articles = []
    for url in input_ids:
        if url != '':
            input_articles.append(url)
        else:
            input_ids.remove(url)

    input_articles = tvrain_data.get_articles_data(input_articles)

    # First time we need to fit model
    if not model_init:
        model.init(tvrain_data)
        model_init = True

    result = model.predict(
        input_articles=input_articles,
        input_ids=input_ids,
        tvrain_data=tvrain_data,
        recommends_num=recommends_num
    )
    output_articles = []
    for raw in result:
        article_data = tvrain_data.collection.find_one({'_id': raw[0]})
        output_articles.append({
            'title': article_data['title'],
            'url': article_data['url']
        })
    return output_articles
