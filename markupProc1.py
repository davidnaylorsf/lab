
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup

def processMarkup(markupDocument):
  markup = markupDocument["markup"]
  string = markupDocument["string"]
  stringLength = len(string)
  for markupItem in markup:
    start = markupItem["Start"]
    length = markupItem["Length"]
    if "Type" in markupItem:
      type = markupItem["Type"]
      extractString = string[start:start+length]
      if type == "Italics":        
        italicLength = length
      elif type == "Superscript":
        superscriptLength = length
      elif type == "Subscript":
        subscriptLength = length
      elif type == "Image":
        imageURL = markupItem["URL"]
        imageSize = markupItem["Size"]
        imageCaption = markupItem["Caption"]
        imageLength = length                      
      else:
        print("Unhandled markup type:" + str(type))


# markups = coll.find({"RecordNumber": 1})
markups = coll.find({})
retrievedCount = markups.retrieved

for markupDoc in markups:
  
  processMarkup(markupDoc)
  markup = markupDoc["markup"]
  string = markupDoc["string"]
  
  markupRecTitle = markupDoc["RecordTitle"]
