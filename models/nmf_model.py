from collections import Counter
from models.features.topics import topics_similarity
from sklearn.ensemble import RandomForestClassifier


clf = RandomForestClassifier()

generate_features = lambda data: topics_similarity(data)


def generate_data(data):
    x = []
    y = []
    print('Start generate features.')
    for urls in data.sequences.find().limit(-1):
        for url in urls['urls']:
            _id = data.get_article_id(url)
            print(_id)
            x.append(generate_features(_id))
        y.append(1)
    print('Start generate random data.')
    len_true_data = len(x)
    for a in range(0, len_true_data):
        x.append(generate_features(data.get_random_articles()))
        y.append(0)

    return x, y


def init(data):
    clf.fit(*generate_data(data))


def predict(input_articles, input_ids, tvrain_data, recommends_num):
    result_counter = Counter()
    base_features = []
    # Gen for input articles
    for article in input_articles:
        base_features.extend(generate_features(article))

    # Gen for articles in Mongo
    for article in tvrain_data.iterate_articles(except_articles=input_ids):
        result = clf.predict_proba(base_features + generate_features(article))
        result_counter[article['_id']] = result[1] 
    
    return list(result_counter.most_common(recommends_num))
