# pip intall logtail-python
from logtail import LogtailHandler
import logging
from src.constants import BETTERSTACK_TOKEN
from pythonjsonlogger import jsonlogger
from src.mongodb_func import MongoDBHandler


def logging_better_stack(log_level: int) -> logging.Logger:
    logger = logging.getLogger("better_stack")
    logger.setLevel(log_level)  # logging.DEBUG
    logger.handlers = []
    better_stack_handler = LogtailHandler(source_token=BETTERSTACK_TOKEN)
    json_format = jsonlogger.JsonFormatter(
        "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
        rename_fields={"levelname": "severity", "asctime": "timestamp"},
        datefmt="%Y-%m-%dT%H:%M:%SZ")
    better_stack_handler.setFormatter(json_format)
    logger.addHandler(better_stack_handler)
    return logger


def logging_mongodb(log_level: int, host, port, database, collection) -> logging.Logger:
    logger = logging.getLogger("mongodb")
    logger.setLevel(log_level)  # logging.DEBUG
    logger.handlers = []
    mongo_handler = MongoDBHandler(host, port, database, collection)
    logger.addHandler(mongo_handler)
    return logger
