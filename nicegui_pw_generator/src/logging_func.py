# pip intall logtail-python
from logtail import LogtailHandler
import logging
from src.constants import BETTERSTACK_TOKEN


def logging_better_stack(log_level: int) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)  # logging.DEBUG
    logger.handlers = []
    better_stack_handler = LogtailHandler(source_token=BETTERSTACK_TOKEN)
    logger.addHandler(better_stack_handler)
    return logger
