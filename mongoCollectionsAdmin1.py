from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.239:27017/')
db = client.Elements_PubChem
collectionNames = db.list_collection_names()

sectionCollectionNames = ['History', 'Sources', 'Properties', 'Isotopes', 'Identifiers', 'References',  'Uses',  'Compounds', 'Description']

for collectionName in sectionCollectionNames:
  # Print Document Count by Collection Name
  docCount = db[collectionName].estimated_document_count()
  print("Collection: " + collectionName + " holds " + str(docCount) + " documents.")

  # Clear Collections by Name - Uncomment as needed
  # db[collectionName].delete_many({})
  # docCount = db[collectionName].estimated_document_count()
  # print("Collection: " + collectionName + " holds " + str(docCount) + " documents.")