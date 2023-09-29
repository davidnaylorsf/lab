# Working through examples of:
# https://mixedanalytics.com/knowledge-base/filter-specific-fields-values/


import jmespath as jp
import json

with open('input_example2.json') as f:
    data = json.load(f)

# Example2

query2 = "data[].{amount:amount,billing_email:billing_details.{email:email,location:location}}"
query2a = "data[].{amount:amount,billing_email:billing_details.{em:email,loc:location}}"

example2 = jp.search(query2, data)
example2a = jp.search(query2a, data)

print(str(example2))