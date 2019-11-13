from time import time
from typing import Any
from logger import logger
from functools import wraps


class SysMetrics:
    @classmethod
    def execution_time(cls, action: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start = time()
                result = func(*args, **kwargs)
                end = time()
                logger.info(f'Время выполнения метода [{action}] = {end - start} сек.')
                return result
            return wrapper
        return decorator
