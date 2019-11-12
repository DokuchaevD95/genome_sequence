import os
import logging
from config import config


__all__ = ['logger']


logger = logging.getLogger('app')


_LOG_PATH = config['log_path']
_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(filename)s: %(message)s'

# Создание директории и файла, если они не существуют
if not os.path.exists(_LOG_PATH):
    dir_name = os.path.dirname(_LOG_PATH)
    os.makedirs(dir_name)
    with open(_LOG_PATH, 'w'):
        pass


_FILE_HANDLER = logging.FileHandler(_LOG_PATH)
_STREAM_HANDLER = logging.StreamHandler()

# LEVEL configuring
_FILE_HANDLER.setLevel(logging.WARNING)
_STREAM_HANDLER.setLevel(logging.WARNING)

# SET FORMATTER
_FILE_HANDLER.setFormatter(logging.Formatter(_LOG_FORMAT))
_STREAM_HANDLER.setFormatter(logging.Formatter(_LOG_FORMAT))

# ADD HANDLERS
logger.addHandler(_FILE_HANDLER)
logger.addHandler(_STREAM_HANDLER)
