"""
Get predictions by ids of user's news
"""
from models import nmf_model

model = nmf_model
model_init = False


def predict(first_id=None, second_id=None, third_id=None,
            tvrain_data=None, recommends_num=3):
    """
    Get news predictions. If one of ids isn't specified,
    so replace it to most popular articles. If none of ids
    is specified, get most popular news.
    :param first_id: MongoDB id of first article
    :param second_id:
    :param third_id:
    :param tvrain_data: data.data_utils.TvrainData object
    :param recommends_num: num of articles to recommend
    :return: [{'id': '', 'url': '', 'title': ''}, ...]
    """
    global model_init
    
    input_ids = [first_id, second_id, third_id]
    input_articles = tvrain_data.get_articles_data([
        first_id, second_id, third_id
    ])
    
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
    for object_id in result:
        article_data = tvrain_data.find_one({'_id': object_id})
        output_articles.append({
            'title': article_data['title'],
            'url': article_data['url']
        })
    return output_articles
