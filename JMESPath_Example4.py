# Working through examples of:
# https://mixedanalytics.com/knowledge-base/filter-specific-fields-values/


import jmespath as jp
import json

with open('input_example4.json') as f:
    data = json.load(f)

# Example4
query4 = "locations[?state == 'NY']"
query4a = "locations[?name == 'Bellevue']"
query4b = "locations[?name == 'Bellevue' || state == 'NY']"

example4 = jp.search(query4, data)
example4a = jp.search(query4a, data)
example4b = jp.search(query4b, data)

print(str(example4))