import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

mongo_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))