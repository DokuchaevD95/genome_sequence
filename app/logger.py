import os
import logging
from config import config


__all__ = ['logger']


logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

_LOG_PATH = config['log_path']
_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(filename)s : %(message)s'

# Создание директории и файла, если они не существуют
if not os.path.exists(_LOG_PATH):
    dir_name = os.path.dirname(_LOG_PATH)
    os.makedirs(dir_name)
    with open(_LOG_PATH, 'w'):
        pass


_FILE_HANDLER = logging.FileHandler(_LOG_PATH)
_STREAM_HANDLER = logging.StreamHandler()

# LEVEL configuring
_FILE_HANDLER.setLevel(logging.DEBUG)
_STREAM_HANDLER.setLevel(logging.DEBUG)

# Create formatter
_FILE_FORMATTER = logging.Formatter(_LOG_FORMAT)
_STREAM_FORMATTER = logging.Formatter(_LOG_FORMAT)

# SET FORMATTER
_FILE_HANDLER.setFormatter(_FILE_FORMATTER)
_STREAM_HANDLER.setFormatter(_STREAM_FORMATTER)

# ADD HANDLERS
logger.addHandler(_STREAM_HANDLER)
logger.addHandler(_FILE_HANDLER)
