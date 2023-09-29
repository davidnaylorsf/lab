# Working through examples of:
# https://mixedanalytics.com/knowledge-base/filter-specific-fields-values/


import jmespath as jp
import json

with open('input_example5.json') as f:
    data = json.load(f)

# Example5
query5 = "data.*.{id:id,name:name,cmc_rank:cmc_rank}|[?cmc_rank<=`5`]"

example5 = jp.search(query5, data)


print(str(example5))