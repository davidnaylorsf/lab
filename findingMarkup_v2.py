import jmespath as jp
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.Markup
updateDB = True

def getRecord(recordNumber, sourceData):
    # Returns the first matching Record that matches the filter
    queryStr = "[*].Record | [?RecordNumber == `" + str(recordNumber) + "`]"
    record = jp.search(queryStr , sourceData)
    return record[0]

with open('ELEMENTS_v2.json') as f:
    data = json.load(f)

for recordNumber in range(1,21):
    
    record = getRecord(recordNumber, data)
    recType = jp.search("RecordType" , record)
    recNumber = jp.search("RecordNumber" , record)
    recTitle = jp.search("RecordTitle" , record)
    # record_meta in preparation for adding
    record_meta = {'RecordType': recType, 'RecordNumber': recNumber, 'RecordTitle': recTitle}

    sections = jp.search("Section" , record)
    InformationQuery = "Section[].Information"
    # InformationQuery2 = "[ RecordTitle , Section[].Information]"
    informations = jp.search(InformationQuery , record)
    # informations2 = jp.search(InformationQuery2 , record)
    ValueQuery = "Section[].Information[].Value"
    values = jp.search(ValueQuery, record)
    SWMQuery = "Section[].Information[].Value[].StringWithMarkup"
    swmqs = jp.search(SWMQuery, record)
    RSI_MarkupQuery = "Section[].Information[].Value[].StringWithMarkup[].Markup"
    markups1 = jp.search(RSI_MarkupQuery, record)
    RSSI_MarkupQuery = "Section[].Section[].Information[].Value[].StringWithMarkup[].Markup"
    markups2 = jp.search(RSSI_MarkupQuery, record)

    if updateDB:
      if markups1 is not None: 
        if len(markups1) > 0:
          for markup in markups1:
             for markup_item in markup:
                markup_item['RecordTitle']=recTitle
                markup_item['RecordNumber']=recNumber
                markup_id = db.Markup.insert_one(markup_item).inserted_id

      if markups2 is not None: 
        if len(markups2) > 0:
          for markup in markups2:
             for markup_item in markup:
                markup_item['RecordTitle']=recTitle
                markup_item['RecordNumber']=recNumber
                markup_id = db.Markup.insert_one(markup_item).inserted_id


    # print(str(len(informations)))
    # Comment
