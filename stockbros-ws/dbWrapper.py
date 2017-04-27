#!flask/bin/python
from pymongo import MongoClient

#Mongodb Conf
MONGODB_HOST = 'localhost'
MONGODB_PORT = '27017'
client = MongoClient('mongodb://' + MONGODB_HOST + ':' + MONGODB_PORT + '/')
db = client['StockBros']