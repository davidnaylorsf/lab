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

for recordNumber in range(6, 21):

    record = getRecord(recordNumber, data)

    sections = jp.search("[0].Section" , record)
    TOCHeadings = jp.search("[*].TOCHeading", sections)

    identifiers = flatten_json(jp.search( "[0]", sections))
    properties = flatten_json(jp.search( "[1]", sections))
    history = flatten_json(jp.search( "[2]", sections))
    description = flatten_json(jp.search( "[3]", sections))
    uses = flatten_json(jp.search( "[4]", sections))
    sources = flatten_json(jp.search( "[5]", sections))
    compounds = flatten_json(jp.search( "[6]", sections))
    isotopes = flatten_json(jp.search( "[6]", sections))
    references = flatten_json(jp.search("[0].Reference" , record))

    identifiers_id = db.Identifiers.insert_one(identifiers).inserted_id
    properties_id = db.Properties.insert_one(properties).inserted_id
    history_id = db.History.insert_one(history).inserted_id
    description_id = db.Description.insert_one(description).inserted_id
    uses_id = db.Uses.insert_one(uses).inserted_id
    sources_id = db.Sources.insert_one(sources).inserted_id
    compounds_id = db.Compounds.insert_one(compounds).inserted_id
    isotopes_id = db.Isotopes.insert_one(isotopes).inserted_id
    references_id = db.References.insert_one(references).inserted_id

print(identifiers_id)