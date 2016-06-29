from collections import Counter
import datetime

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle

from models.features.topics import topics_similarity

clf = RandomForestClassifier()


def generate_features(data, val=None):
    features = []
    for raw in data:
        features.extend(topics_similarity(raw))

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

        if len(features[0]) == 160:
            x_true.append(features[0])
            y_true.append(features[1])
        else:
            print(features, urls)

    print('Start generate random data.')
    while len(x_true) != len(x_false):
        features = generate_features(data.get_random_articles(4), 0)

        if len(features[0]) == 160:
            x_false.append(features[0])
            y_false.append(features[1])
        else:
            print(features)
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
    clf.fit(x, y)


def predict(input_articles, input_ids, tvrain_data, recommends_num):
    result_counter = Counter()
    base_features = []
    # Gen for input articles
    base_features.extend(generate_features(input_articles))
    min_time = input_articles[0]['time'] - datetime.timedelta(hours=5)
    max_time = input_articles[-1]['time'] + datetime.timedelta(hours=5)
    mongo_query = {'time': {'$gte': min_time, '$lt': max_time}}
    # Gen for articles in Mongo
    for article in tvrain_data.iterate_articles(except_articles=input_ids, query=mongo_query):
        new_features = base_features + generate_features([article])
        result = clf.predict_proba([new_features])
        result_counter[article['_id']] = result[0][1]
    return list(result_counter.most_common(recommends_num))

