from logger import logger
from typing import Optional
from .base import BaseSubSeqSearcher, SubSeqInfo
from concurrent.futures import ProcessPoolExecutor


class BrutePairSearcher(BaseSubSeqSearcher):
    WORKERS = 3

    def search(self, initial_len: int = 1) -> SubSeqInfo:
        result = None
        start_first = 0
        for curr_len in range(initial_len, self.max_length):
            sub_info = self._check_len(curr_len, start_first)
            if not sub_info:
                return result
            else:
                logger.info(sub_info)
                start_first = sub_info.first_beg
                result = sub_info

    def _check_len(self, length: int, start_first: int = 0) -> Optional[SubSeqInfo]:
        logger.info(f'Проверка длины {length}')
        for i in range(start_first, len(self.first) - length):
            for j in range(0, len(self.second) - length):
                first_sub = self.first[i:i+length]
                second_sub = self.second[j:j+length]

                if first_sub == second_sub:
                    return SubSeqInfo(length, i, j)
        return None
