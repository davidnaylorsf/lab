
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup

def processMarkup(markupDocument):
  markup = markupDocument["markup"]
  string = markupDocument["string"]
  newString = string
  startAddition = 0

  for markupItem in markup:
    start = markupItem["Start"]
    length = markupItem["Length"]
    
    if "Type" in markupItem:
      type = markupItem["Type"]
      extractString = newString[start+startAddition:start+startAddition+length]
      if type == "Italics":        
        newString = newString[:start+startAddition] + "<em>" + extractString + "</em>" + newString[start+startAddition+length:]
        #Update the value of startAddition to correct for inserted text
        startAddition = startAddition + 9
        print(newString)
      elif type == "Superscript":
        newString = newString[:start+startAddition] + "<sup>" + extractString + "</sup>" + newString[start+startAddition+length:]
        startAddition = startAddition + 11        
      elif type == "Subscript":
        newString = newString[:start+startAddition] + "<sub>" + extractString + "</sub>" + newString[start+startAddition+length:]
        startAddition = startAddition + 11 
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
  

