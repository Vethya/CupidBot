from pymongo import MongoClient
from cupid import config

cli = MongoClient(config['config']['mongo_uri'])
