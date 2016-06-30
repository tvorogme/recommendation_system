from collections import Counter
import datetime

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle

from models.features.topics import topics_similarity
from models.features.cosine import cosine_similarity_features

clf = RandomForestClassifier()
clf_one = RandomForestClassifier()
clf_two = RandomForestClassifier()

def generate_features(data, val=None):
    features = []
    for raw in data:
        features.extend(topics_similarity(raw))
    features.extend(cosine_similarity_features(data[:-1], data[-1]))

    if val is None:
        return features
    else:
        return features, val


def generate_data(data):
    x_true = []
    y_true = []
    x_false = []
    y_false = []
    print('Start generate features.')
    for urls in data.sequences.find():
        features = generate_features(data.get_articles_data(urls['urls']), 1)
        x_true.append(features[0])
        y_true.append(features[1])

    print('Start generate random data.')
    while len(x_true) != len(x_false):
        features = generate_features(data.get_random_articles(4), 0)
        x_false.append(features[0])
        y_false.append(features[1])

    return x_true + x_false, y_true + y_false


def init(data):
    try:
        x = np.load(open('train_x.np', 'rb'))
        y = np.load(open('train_y.np', 'rb'))
    except FileNotFoundError:
        x, y = generate_data(data)
        np.save(open('train_x.np', 'wb'), x)
        np.save(open('train_y.np', 'wb'), y)
    x, y = shuffle(x, y)
    x_one = list(map(lambda a: a[:81], x))
    x_two = list(map(lambda a: a[:121], x))

    print('Train model for 3 articles.')
    clf.fit(x, y)

    print('Train model for 1 article.')
    clf_one.fit(x_one, y)

    print('Train model for 2 articles.')
    clf_two.fit(x_two, y)


def predict(input_articles, input_ids, tvrain_data, recommends_num):
    result_counter = Counter()
    min_time = input_articles[0]['time'] - datetime.timedelta(hours=5)
    max_time = input_articles[-1]['time'] + datetime.timedelta(hours=5)
    mongo_query = {'time': {'$gt': min_time, '$lt': max_time}}
    len_articles = len(input_articles)
    # Gen for articles in Mongo
    for article in tvrain_data.iterate_articles(except_articles=input_ids, query=mongo_query):
        new_features = generate_features(input_articles + [article])
        if len_articles == 3:
            result = clf.predict_proba([new_features])
        elif len_articles == 2:
            result = clf_two.predict_proba([new_features])
        elif len_articles == 1:
            result = clf_one.predict_proba([new_features])
        result_counter[article['_id']] = result[0][1]
    return list(result_counter.most_common(recommends_num))
