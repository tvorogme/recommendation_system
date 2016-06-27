#!/usr/bin/env python
# coding=utf-8
import os
import random
from pymongo import MongoClient


class TvrainData():
    def __init__(self):
        '''
        :param data: Pandas Frame with data.
        Just load data from Mongo.
        '''   
        self.dataframe = MongoClzient(os.environ['MONGODB_URL']).tvrain.articles

    def get_random_articles(self, n):
        '''Returns N of topics for index.html'''
        all_articles = self.dataframe.find({}, {'time': 1})
        randomint = random.randint(1, all_articles.count())
        sorted_items = all_articles.sort('time', 1)[randomint:randomint+5]
        return [i for i in sorted_items]

