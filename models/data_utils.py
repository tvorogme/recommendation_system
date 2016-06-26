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
        mongodb_items = list(MongoClient(os.environ['MONGODB_URL']).tvrain.tvrain.find())
        self.dataframe = pd.DataFrame.from_dict(mongodb_items)
        
        # This shit is about mongo can't save id -> str.
        self.dataframe._id = list(map(lambda _id: str(_id), self.dataframe._id.values))

    def get_random_by_tume(self, n):
        '''Returns N of topics for index.html'''
        sorted_time = sorted(self.datafram.time.values)
        # We need indexes for slice in time
        index = sorted_time.index(random.choice(sorted_time))
        times = sorted(self.dataframe.time.values)[index:index+n]

        out_values = []
        for val in self.dataframe[self.dataframe.time.isin(times)].values:
            out_values.append({'value': val[0], 'desc': val[3]})

        return out_values
