import numpy as np
import pandas as pd
import jmespath as jp
import json

def getRecord(recordNumber, sourceData):
    queryStr = "[*].Record | [?RecordNumber == `" + str(recordNumber) + "`]"
    record = jp.search(queryStr , sourceData)
    return record

with open('ELEMENTS_v2.json') as f:
    data = json.load(f)

record = getRecord(18, data)

sections = jp.search("[0].Section" , record)
references = jp.search("[0].Reference" , record)

TOCHeadings = jp.search("[*].TOCHeading", sections)
identifiers = jp.search( "[0]", sections)
properties = jp.search( "[1]", sections)
history = jp.search( "[2]", sections)
description = jp.search( "[3]", sections)
uses = jp.search( "[4]", sections)
sources = jp.search( "[5]", sections)
compounds = jp.search( "[6]", sections)
isotopes = jp.search( "[6]", sections)




