import os
import sys
import csv
from pymongo import MongoClient

print('Parsing topics')
topics = {}
with open(sys.argv[1], 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if line[0] == 1:
            continue
        topics[line[0]] = line[1:]

print('Connecting to MongoDB')
mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
articles = db.articles

for article in topics:
    articles.update({'_id': article}, {'$set': {
        'topics': topics[article]
    }})
