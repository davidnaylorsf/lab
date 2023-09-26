import numpy as np
import pandas as pd
import jmespath as jp
import json

def getRecord(recordNumber, sourceData):
    queryStr = "[0:15].Record | [?RecordNumber == `" + str(recordNumber) + "`]"
    record = jp.search(queryStr , sourceData)
    return record

with open('ELEMENTS_v2.json') as f:
    data = json.load(f)

record = getRecord(2, data)

idList = jp.search("[1:3]._id", data)
recordList = jp.search("[1:3].Record", data)



