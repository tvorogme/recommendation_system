import os
import time
import datetime
import re

import requests
from lxml import html
from pymongo import MongoClient

month_dict = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12
}
year_re = re.compile(r'\d+')


def parse_date(tvrain_date_str):
    splits = tvrain_date_str.lower().split()
    if year_re.match(splits[-1]) is not None:
        year = int(splits[-1])
        month = month_dict[splits[-2]]
        day = int(splits[0])
        return datetime.datetime(year=year, month=month, day=day)
    else:
        year = datetime.datetime.now().year
        month = month_dict[splits[-1]]
        day = int(splits[-2])
        if len(splits) > 2:
            hours, minutes = splits[0].rstrip(",").split(":")
        else:
            hours, minutes = (0,0)
        return datetime.datetime(year=year, month=month, day=day, hour=int(hours), minute=int(minutes))


mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
articles = db.articles


for article in articles.find():
    url = article['url']
    response = requests.get(url)
    tree = html.fromstring(response.text)
    pub_date = tree.xpath("//div[@class='meta__value']/span/text()")
    try:
        pub_date_py = parse_date(pub_date[0].encode('utf-8'))
    except ValueError:
        print(pub_date[0])
        break
    timestamp = time.mktime(pub_date_py.timetuple())
    articles.update({'_id': article['_id']}, {'$set': {'datetime': timestamp}})

