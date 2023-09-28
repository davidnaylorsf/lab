
import jmespath as jp
import json
from pymongo import MongoClient
from genson import SchemaBuilder

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
coll = db.ElementSchema

with open('ELEMENTS_v2.json') as f:
    data = json.load(f)

builder = SchemaBuilder()
builder.add_schema({"type": "object", "properties": {}})
builder.add_object(data)

ElementsSchema = builder.to_schema()

size = ElementsSchema.__sizeof__()
print("Size of Schema is: " + str(size))

SchemaProperties = ElementsSchema["anyOf"][1]["items"]["properties"]["Record"]

schema_id = coll.insert_one(SchemaProperties).inserted_id
print("schema_id: " + str(schema_id))

