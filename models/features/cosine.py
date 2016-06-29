import os


def cosine_similarity(intersection_num, all_items_num,
                      first_set_len, second_set_len):
    """
    Count cosine similarity based on intersection data
    :param intersection_num: len of intersection of two sets
    :param all_items_num: num of all items, for example, sum of views
    :param first_set_len: len of first set, for example, views of first video
    :param second_set_len:
    :return:
    """
    intersection_probability = (intersection_num / all_items_num) ** 2
    first_set_probability = first_set_len / all_items_num
    second_set_probability = second_set_len / all_items_num
    cosine_similarity_value = (
        intersection_probability /
        (first_set_probability * second_set_probability)
    )
    return cosine_similarity_value


def cosine_similarity_features(input_articles, output_article):
    """
    Generate features for input articles and possible recommended article
    :param input_articles: list of MongoDB documents
    :param output_article: MongoDB documents
    :return: list of features
    """
    features = []
    output_article_views = set(output_article['views'])
    for input_article in input_articles:
        input_article_views = set(input_article['views'])
        result = cosine_similarity(
            intersection_num=len(output_article_views.intersection(input_article_views)),
            all_items_num=int(os.environ['ALL_USERS_NUM']),
            first_set_len=len(output_article_views),
            second_set_len=len(input_article_views)
        )
        features.append(result)
    print(len(input_articles), features)
    return features
