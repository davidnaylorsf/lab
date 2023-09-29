# Working through examples of:
# https://mixedanalytics.com/knowledge-base/filter-specific-fields-values/


import jmespath as jp
import json

with open('iTunes1.json') as f:
    data = json.load(f)

# Example1

query1 = "results[].{tracks:trackName,collections:collectionName}"
query1a = "results.{tracks:trackName,collections:collectionName}"
query1b = "results[*].{tracks:trackName,collections:collectionName}"


example1 = jp.search(query1, data)
example1a = jp.search(query1a, data)
example1b = jp.search(query1b, data)

print(str(example1))
