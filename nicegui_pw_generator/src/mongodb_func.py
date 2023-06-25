from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.collection import Collection
from typing import TypedDict
from bson.objectid import ObjectId
from bson.son import SON
import logging
from src.retrieve_datetime import current_date_jst

class Logs(TypedDict):
    filenmae: str
    lineno: int
    message: str
    name: str
    process: int
    severity: str
    timestamp: str


def mondodb_client_collection(
        host: str,
        port: int,
        class_name: object,
        db_name: str,
        collection_name: str
) -> Collection:
    client: MongoClient = MongoClient(host, port)
    db: Database[class_name] = client[db_name]  # db name
    collection: Collection[class_name] = db[collection_name]  # collection name
    return collection


class MongoDBHandler(logging.Handler):
    def __init__(self, host, port, database, collection):
        logging.Handler.__init__(self)
        self.client = MongoClient(host, port)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def emit(self, record):
        log_entry = {
            "name": record.name,
            "pathname": record.pathname,
            "module": record.module,
            "function": record.funcName,
            "filename": record.filename,
            "lineno": record.lineno,
            "message": self.format(record),
            "level": record.levelname,
            "dt": current_date_jst(),
            "process": record.process

        }
        self.collection.insert_one(log_entry)
