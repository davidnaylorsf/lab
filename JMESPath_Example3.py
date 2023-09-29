# Working through examples of:
# https://mixedanalytics.com/knowledge-base/filter-specific-fields-values/


import jmespath as jp
import json

with open('iTunes1.json') as f:
    data = json.load(f)

# Example3
query3 = "{results_count:resultCount,results:results[].{artistName:artistName,trackName:trackName}}"
query3a = "[{result_count:resultCount},results[].{artistName:artistName,trackName:trackName}]"

example3 = jp.search(query3, data)
example3a = jp.search(query3a, data)

print(str(example3))