import os
import sys
import csv

from pymongo import MongoClient
from bson.objectid import ObjectId

print('Parsing topics')
topics = {}
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if line[0] == '':
            continue
        topics[line[0]] = list(map(float, line[1:]))

print('Connecting to MongoDB')
mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
articles = db.articles

print(articles.find({'topics': {'$exists': True}}).count())

for article in topics:
    articles.update({'_id': ObjectId(article)}, {'$set': {
        'topics': topics[article]
    }})
