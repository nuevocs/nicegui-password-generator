import random
import string
import logging
from src import logging_func

logger: logging.Logger = logging_func.logging_better_stack(30)  # WARNING=30

# Generate a random password
def generating_random_password(
        punctuation_flag: bool = False,
        password_length: int = 16
) -> str:
    assert password_length > 2, logger.error("Password length must be greater than 2")
    match punctuation_flag:
        case True:
            total = string.ascii_letters + string.digits + string.punctuation
        case False:
            total = string.ascii_letters + string.digits

    length = password_length
    password = "".join(random.sample(total, length))
    return password
