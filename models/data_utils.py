#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import os
import random
from pymongo import MongoClient


class TvrainData:
    def __init__(self):
        '''
        :param data: Pandas Frame with data.
        Just load data from Mongo.
        '''
        self.data = pd.DataFrame.from_dict(list(MongoClient(os.environ['MONGODB_URL']).tvrain.tvrain.find()))
        # This shit is about mongo can't save id -> str.
        self.data._id = list(map(lambda _id: str(_id), self.data._id.values))

    def get_random_by_tume(self, n):
        '''Returns N of topics for index.html'''
        sorted_time = sorted(self.data.time.values)
        # We need indexes for slice in time
        index = sorted_time.index(random.choice(sorted_time))
        times = sorted(self.data.time.values)[index:index+n]

        out_values = []
        for val in self.data[self.data.time.isin(times)].values:
            out_values.append({'value': val[0], 'desc': val[3]})

        return out_values
