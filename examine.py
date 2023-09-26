import numpy as np
import pandas as pd
import json


df = pd.read_json('.jupyter/lab/ELEMENTS_v2.json')

columns = df.columns
records = df['Record']
sections = records[0]['Section']

df.head()

