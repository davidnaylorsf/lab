
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup

markups = coll.find({"RecordNumber": 1})

for markupDoc in markups:
  markup = markupDoc["markup"]
  string = markupDoc["string"]
  
  markupRecTitle = markupDoc["RecordTitle"]
