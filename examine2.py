import numpy as np
import pandas as pd
import json

with open('.jupyter/lab/ELEMENTS_v2.json') as f:
    data = json.load(f)

records=[]

for recordRow in data:
    record = recordRow['Record']
    records.append(record)

sections=[]

for record in records:
    section = record['Section']
    sections.append(section)



dh = data.head()