#!/usr/bin/env python
# coding=utf-8
import os
from pymongo import MongoClient
import random

class TvrainData():
    def __init__(self):
        """
        :param data: Pandas Frame with data.
        Just load data from Mongo.
        """
        self.collection = MongoClient(os.environ['MONGODB_URL']).tvrain.articles
        self.collection.create_index("time")

    def get_random_articles(self, n):
        """Returns N of topics for index.html"""
        articles = self.collection.find({}, {'url': 1, 'time': 1, 'title': 1}).skip(random.randint(0,self.collection.count())).limit(10)
        return list(articles)

    def get_articles_data(self, articles_ids):
        """
        Get data from MongoDB for articles_ids
        :param articles_ids: ['article_id', ...]
        :return: list of MongoDB documents
        """
        raise NotImplemented()

    def iterate_articles(self, except_articles):
        """
        Iteate throw all articles without ids of except articles
        :param except_articles: list of ids
        :return:
        """
        raise NotImplemented()


