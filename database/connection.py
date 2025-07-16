from pymongo import MongoClient
import os

Mongo_URL = os.getenv("Mongo_URL", "mongodb://localhost:27017/")
client = MongoClient(Mongo_URL)
db = client["planner_db"]

