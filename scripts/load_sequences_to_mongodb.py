import os
import sys
import json
from pymongo import MongoClient

print('Parsing sequences')
with open(sys.argv[1], 'r') as sequences_file:
    sequences = json.loads(sequences_file.read())

print('Connecting to MongoDB')
mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
sequences_collection = db.sequences

for sequence in sequences:
    sequences_collection.insert_one({
        'urls': sequence
    })
