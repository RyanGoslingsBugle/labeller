from pymongo import MongoClient

client = MongoClient()
db = client.__DB_NAME__
collection = db.__COLLECTION_NAME__

tweet_schema = [
    __LIST_OF_FIELD_NAMES__
]