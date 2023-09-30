
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup

def processMarkup(markupDocument):
  markup = markupDocument["markup"]
  string = markupDocument["string"]
  stringLength = len(string)
  newString = string
  startAddition = 0
  markupItemCount = len(markup)
  # if markupItemCount > 4:
    # print(string)
  for markupItem in markup:
    start = markupItem["Start"]
    length = markupItem["Length"]
    
    if "Type" in markupItem:
      type = markupItem["Type"]
      extractString = newString[start+startAddition:start+startAddition+length]
      if type == "Italics":        
        italicLength = length
        newString = newString[:start+startAddition] + "<em>" + extractString + "</em>" + newString[start+startAddition+length:]
        #Update the value of startAddition to correct for inserted text
        startAddition = startAddition + 9
        print(newString)
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

  htmlString = "<span>" + newString + "</span>"
  return htmlString


# markups = coll.find({"RecordNumber": 1})
markups = coll.find({})
retrievedCount = markups.retrieved

for markupDoc in markups:
  
  htmlString = processMarkup(markupDoc)
  markup = markupDoc["markup"]
  string = markupDoc["string"]
  
  markupRecTitle = markupDoc["RecordTitle"]
