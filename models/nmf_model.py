from collections import Counter
from models.features.topics import topics_similarity
import random

clf = None


def init():
    # Load clf here
    pass


def predict(input_articles, input_ids, tvrain_data, recommends_num):
    result_counter = Counter()
    base_features = []
    for article in input_articles:
        base_features.extend(topics_similarity(article))
    for article in tvrain_data.iterate_articles(except_articles=input_ids):
        result = clf.predict_proba(base_features + topics_similarity(article))
        result_counter[article['_id']] = result[1]
    return list(result_counter.most_common(recommends_num))
