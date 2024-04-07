from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy


mongodb = PyMongo(connect=True)
sqlalchemy_db = SQLAlchemy()


class MongoCollections:
    TRADE_REQUESTS_COLLECTION = "trade_requests"
