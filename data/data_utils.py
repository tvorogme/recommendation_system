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
        self.sequences = MongoClient(os.environ['MONGODB_URL']).tvrain.sequences
        self.collection = MongoClient(os.environ['MONGODB_URL']).tvrain.articles
        self.collection.create_index("time")


    def get_random_articles(self, n):
        """Returns N of topics for index.html"""
        articles = self.collection.find().skip(random.randint(0,self.collection.count())).limit(n)
        return list(articles)

    def get_article_id(self, url):
        """Get id by url"""
        self.collection.find({'url': url}).limit(-1)

    def get_articles_data(self, articles_ids):
        """
        Get data from MongoDB for articles_ids
        :param articles_ids: ['article_id', ...]
        :return: list of MongoDB documents
        """
        articles_data = []
        for i in articles_ids:
            articles_data.extend(list(self.collection.find({'url': i}).limit(-1)))

        return articles_data

    def iterate_articles(self, except_articles=[], skip=0):
        """
        Iteate throw all articles without ids of except articles
        :param except_articles: list of ids
        :return:
        """
        for value in self.collection.find().skip(skip).limit(-1):
            if value not in except_articles:
                yield value

    def get_sequences(self):
        """Return all sequences for train"""
        return list(self.sequences.find().limit(-1))

