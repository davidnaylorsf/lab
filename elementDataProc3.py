# Read Element data from a local file
# Extract sections and subsections of interest
# Write selected sections and subsections to a Mongo collection

# Local file is ELEMENTS_v2.json
# MongoDB db_name is Elements_PubChem
# MongoDB coll_name is ElementSections

import jmespath as jp
import json
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.ElementSections


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
    references_ids = db.References.insert_many(references_sect).inserted_ids

    for TOCHeading in TOCHeadings:
        # exampleQuery = "[*] | [?TOCHeading == 'Identifiers']"
        sectionQuery = "[*] | [?TOCHeading == '" + TOCHeading + "']"

        found_sections = jp.search( sectionQuery, sections)
        if len(found_sections) > 1:
            print("Number of found sections for " + str(TOCHeading) + " for " + str(recTitle) + " is " + str(len(found_sections)) + " !")
        # The use of this first_found_section is a temporary approach to aid in debugging
        # and to more easily test the conditions under which more than one is found
        first_found_section = found_sections[0]
        doc_id = db[TOCHeading].insert_one(first_found_section).inserted_id





