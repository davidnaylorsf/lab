import numpy as np
import pandas as pd
import jmespath as jp
import json


with open('ELEMENTS_v2.json') as f:
    data = json.load(f)


result0 = jp.search("[0]", data)
result1 = jp.search("[1:3]", data)

idList = jp.search("[1:3]._id", data)
recordList = jp.search("[1:3].Record", data)

result2 = jp.search("[2]", data)

# ELEMENTS_v2.json