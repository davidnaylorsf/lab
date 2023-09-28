import jmespath as jp
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup
updateDB = True

def getRecord(recordNumber, sourceData):
    queryStr = "[*].Record | [?RecordNumber == `" + str(recordNumber) + "`]"
    record = jp.search(queryStr , sourceData)
    return record

with open('ELEMENTS_v2.json') as f:
    data = json.load(f)


for recordNumber in range(1,21):
    
    record = getRecord(recordNumber, data)
    recType = jp.search("[0].RecordType" , record)
    recNumber = jp.search("[0].RecordNumber" , record)
    recTitle = jp.search("[0].RecordTitle" , record)
    # record_meta in preparation for adding
    record_meta = {'RecordType': recType, 'RecordNumber': recNumber, 'RecordTitle': recTitle}

    sections = jp.search("[0].Section" , record)
    sectionQuery = "[*] | [?TOCHeading == 'Description']"
    description = jp.search( sectionQuery, sections)
    information = jp.search("[0].Information" , description)
    value = jp.search("[0].Value" , information)
    stringWithMarkup = jp.search("StringWithMarkup" , value)
    markup = jp.search("[*].Markup" , stringWithMarkup)
    

    if updateDB:
      if markup is not None: 
        print(str(type(markup)))
        if len(markup) > 0:
          print(len(markup))
          markup_ids = db.Markup.insert_many(markup[0]).inserted_ids

    print(str(recTitle))

