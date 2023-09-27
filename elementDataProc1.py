# Read Element data from a local file
# Extract sections and subsections of interest
# Write selected sections and subsections to a Mongo collection

# Local file is ELEMENTS_v2.json
# MongoDB db_name is Elements_PubChem
# MongoDB coll_name is ElementSections

import pandas as pd
import jmespath as jp
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.ElementSections

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[str(name[:-1])] = str(x)

    flatten(y)
    return out

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

# identifiers_norm = pd.json_normalize(identifiers, record_path=['Section']).values().tolist()
# identifiers_norm = pd.json_normalize(identifiers, record_path=['Section'], meta = ['TOCHeading', 'Description'], record_prefix='_').to_json()

identifiers_fl = flatten_json(identifiers)
references_fl = flatten_json(references)
doc_id = coll.insert_one(identifiers_fl).inserted_id
doc_id = coll.insert_one(references_fl).inserted_id

# doc_id = coll.insert_one(identifiers).inserted_id
# doc_ids = coll.insert_many(references).inserted_ids
print(doc_id)