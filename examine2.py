import numpy as np
import pandas as pd
import json

with open('.jupyter/lab/ELEMENTS_v2.json') as f:
    data = json.load(f)

records=[]
sections=[]
dataSections=[]

for recordRow in data:
    record = recordRow['Record']
    records.append(record)

for record in records:
    section = record['Section']
    sections.append(section)

for section in sections:
    for sectionItem in section:
      if hasattr(sectionItem, 'Section'):
        dataSection=sectionItem['Section']   
        dataSections.append(dataSection)
      if hasattr(sectionItem, 'Information'):
        dataSection=sectionItem['Information']   
        dataSections.append(dataSection)        

dh = data.head()