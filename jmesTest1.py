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

result0 = jp.search("[0]", data)
result1 = jp.search("[1:3]", data)
recordResult1 = jp.search("[*].Record.RecordTitle" , data)
recordResult2 = jp.search("[0:15].Record | [?RecordTitle == 'Boron'] " , data)


recordResult3 = jp.search( queryStr1, data)
recordResult4 = jp.search( queryStr2, data)
# [6]['Record']['RecordTitle']

record2 = getRecord(2, data)

idList = jp.search("[1:3]._id", data)
recordList = jp.search("[1:3].Record", data)



