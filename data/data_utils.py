#!/usr/bin/env python
# coding=utf-8
import os
from pymongo import MongoClient
import random


class TvrainData():
    def __init__(self):
        """
        Just load data from Mongo.
        """
        self.sequences = MongoClient(os.environ['MONGODB_URL']).tvrain.sequences
        self.collection = MongoClient(os.environ['MONGODB_URL']).tvrain.articles
        self.collection.create_index("time")

    def get_random_articles(self, n):
        """Returns N of topics for index.html"""
        articles = self.collection.find().skip(random.randint(0, self.collection.count())).limit(n)
        return list(articles)

    def get_article_id(self, url):
        """Get id by url"""
        return self.collection.find_one({'url': url})['_id']

    def get_articles_data(self, articles_urls):
        """
        Get data from MongoDB for articles urls
        :param articles_urls: ['article_url', ...]
        :return: list of MongoDB documents
        """
        articles = []
        for url in articles_urls:
            articles.append(self.collection.find_one({'url': url}))
        return articles

    def iterate_articles(self, except_articles, skip=0, limit=None):
        """
        Iteate throw all articles without ids of except articles
        :param except_articles: list of ids
        :return:
        """
        if limit is None:
            data = self.collection.find().skip(skip)
        else:
            data = self.collection.find().skip(skip).limit(limit)

        for value in data:
            if value not in except_articles:
                yield value

    def get_sequences(self):
        """Return all sequences for train"""
        return list(self.sequences.find().limit(-1))

