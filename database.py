from flask_pymongo import PyMongo

mongodb = PyMongo(connect=True)


class MongoCollections:
    TRADE_REQUESTS_COLLECTION = "trade_requests"
    USERS_COLLECTION = "users"
