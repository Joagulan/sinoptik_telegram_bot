import json
from pymongo import MongoClient
#a = {'username': 'Павел',
#     'interests': "Гитара, онлайн игры",
 #    'address': 'Кременчуг, Украина'
  #   }
client = MongoClient()
db = client.test_database_bot
collection = db.test_collection_bot
docs = db.docs
#doc_id = docs.insert_one(a).inserted_id
for i in docs.find():
    print(i)
