from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['modlog']

config = db['config']
invites = db['invitetracker']
