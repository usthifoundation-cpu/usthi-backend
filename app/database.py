from pymongo import MongoClient

from app.config import DATABASE_URL, MONGO_DB_NAME

client = MongoClient(DATABASE_URL)
database = client[MONGO_DB_NAME]


def get_db():
    yield database
