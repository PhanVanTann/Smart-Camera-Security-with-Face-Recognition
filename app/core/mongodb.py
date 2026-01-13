import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB = os.getenv("NAME_DB")
print("Mongo URI:", MONGODB_URI)

client = MongoClient(MONGODB_URI)
db = client[MONGO_DB]

residents_collection = db["residents"]