# Import the pymongo library
import pymongo

# Establish a connection to your MongoDB database
client = pymongo.MongoClient("mongodb://raphael:startup@96.22.162.234:27018/?authMechanism=DEFAULT&authSource=FundingBase")

# Select the database and collection you want to work with
db = client["FundingBase"]
collection = db["Sources"]

# Query the collection for all documents
docs = collection.find({})

# Iterate through the documents and print their contents
for doc in docs:
    print(doc)
