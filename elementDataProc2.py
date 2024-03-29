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

for recordNumber in range(1, 21):
    
    record = getRecord(recordNumber, data)
    recType = jp.search("[0].RecordType" , record)
    recNumber = jp.search("[0].RecordNumber" , record)
    recTitle = jp.search("[0].RecordTitle" , record)
    # record_meta in preparation for adding
    record_meta = {'RecordType': recType, 'RecordNumber': recNumber, 'RecordTitle': recTitle}


    sections = jp.search("[0].Section" , record)
    TOCHeadings = jp.search("[*].TOCHeading", sections)

    references_sect = jp.search("[0].Reference" , record)
    references = flatten_json(references_sect)

    references_id = db.References.insert_one(references).inserted_id
    # print("reference_id: " + str(references_id))

    for TOCHeading in TOCHeadings:
        # exampleQuery = "[*] | [?TOCHeading == 'Identifiers']"
        sectionQuery = "[*] | [?TOCHeading == '" + TOCHeading + "']"

        found_sections = jp.search( sectionQuery, sections)
        if len(found_sections) > 0:
          flattened_section = flatten_json(found_sections[0])
          doc_id = db[TOCHeading].insert_one(flattened_section).inserted_id



