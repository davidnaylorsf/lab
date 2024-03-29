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

for recordNumber in range(2, 4):

    record = getRecord(recordNumber, data)

    sections = jp.search("[0].Section" , record)
    TOCHeadings = jp.search("[*].TOCHeading", sections)

    identifiers_sect = jp.search( "[*] | [?TOCHeading == 'Identifiers']", sections)
    properties_sect = jp.search( "[*] | [?TOCHeading == 'Properties']", sections)
    history_sect = jp.search( "[*] | [?TOCHeading == 'History']", sections)
    description_sect = jp.search( "[*] | [?TOCHeading == 'Description']", sections)
    uses_sect = jp.search( "[*] | [?TOCHeading == 'Uses']", sections)
    sources_sect = jp.search( "[*] | [?TOCHeading == 'Sources']", sections)
    compounds_sect = jp.search( "[*] | [?TOCHeading == 'Compounds']", sections)
    isotopes_sect = jp.search( "[*] | [?TOCHeading == 'Isotopes']", sections)
    references_sect = jp.search("[0].Reference" , record)

    # identifiers_old = flatten_json(jp.search( "[0]", sections))

    identifiers = flatten_json(identifiers_sect[0])
    properties = flatten_json(properties_sect[0])
    history = flatten_json(history_sect[0])
    description = flatten_json(description_sect[0])
    uses = flatten_json(uses_sect[0])
    sources = flatten_json(sources_sect[0])
    compounds = flatten_json(compounds_sect[0])
    isotopes = flatten_json(isotopes_sect[0])
    references = flatten_json(references_sect[0])
    

    identifiers_id = db.Identifiers.insert_one(identifiers).inserted_id
    properties_id = db.Properties.insert_one(properties).inserted_id
    history_id = db.History.insert_one(history).inserted_id
    description_id = db.Description.insert_one(description).inserted_id
    uses_id = db.Uses.insert_one(uses).inserted_id
    sources_id = db.Sources.insert_one(sources).inserted_id
    compounds_id = db.Compounds.insert_one(compounds).inserted_id
    isotopes_id = db.Isotopes.insert_one(isotopes).inserted_id
    references_id = db.References.insert_one(references).inserted_id

# print(identifiers_id)