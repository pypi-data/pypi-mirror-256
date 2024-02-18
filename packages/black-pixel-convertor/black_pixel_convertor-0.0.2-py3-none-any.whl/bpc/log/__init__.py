from logging import Logger
from functools import wraps
from datetime import datetime, timedelta

from bpc.log.impl import time_logger, event_logger


def info(message: str, logger: Logger = event_logger):
    logger.info(message)


def warn(message: str, logger: Logger = event_logger):
    logger.warning(message)


def time_log(far_from_utc: int = 9):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_at = datetime.utcnow() + timedelta(hours=far_from_utc)
            info(f"Start at {start_at}", logger=time_logger)

            result = func(*args, **kwargs)

            end_at = datetime.utcnow() + timedelta(hours=far_from_utc)
            info(f"End at {end_at}", logger=time_logger)
            info(f"{end_at - start_at} was spend!", logger=time_logger)

            return result

        return wrapper

    return decorator
