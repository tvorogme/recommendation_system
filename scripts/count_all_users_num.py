import os
from pymongo import MongoClient

mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
articles = db.articles

users = set()

for article in articles.find():
    for user in article['views']:
        users.add(user)

print(len(users))
