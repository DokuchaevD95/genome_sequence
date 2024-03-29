import csv
import math
import pandas
from logger import logger
from utils import SysMetrics
from typing import Optional, List
from .base import BaseSubSeqSearcher, SearchResult


class PairSubSeqSearcher(BaseSubSeqSearcher):
    @SysMetrics.execution_time('Поиск наидлинейшей последовательности методом Царева')
    def tzarev(self, compare_count: int, expected_subseq_size=10**4) -> Optional[SearchResult]:
        """
        Поиск повторяющейся подпоследовательности с частичной
        проверкой начала и конца подпоследовательности
        :param compare_count:
        :param expected_subseq_size:
        :return:
        """

        subseq_info: Optional[SearchResult] = None

        window_size = int(math.sqrt(expected_subseq_size))
        while window_size >= compare_count:
            freq_list = self.get_freq_list(self.first, window_size, window_size)
            dec_freq_list = self.get_freq_list(self.second, window_size, window_size - 1)

            first_freq_item, second_freq_item = self.compare_freq_lists(freq_list, dec_freq_list, compare_count)

            if first_freq_item and second_freq_item:
                logger.info(f'Длина окна k = {window_size}')
                subseq_info = self.allocate_sequences(first_freq_item.beg, second_freq_item.beg)
                subseq_info.k_length = window_size
                break
            else:
                window_size = int(window_size * 0.9)

        return subseq_info

    def _allocate_left_side(self, first_beg: int, second_beg: int) -> int:
        """Определяет длину повтора слева"""

        length = 0
        while first_beg > 0 and second_beg > 0:
            if self.first[first_beg] == self.second[second_beg]:
                length += 1
                first_beg -= 1
                second_beg -= 1
            else:
                break

        return length

    def _allocate_right_side(self, first_beg: int, second_beg: int) -> int:
        """Определяет длину повтора спарва"""

        length = 0
        while (first_beg + 1) < len(self.first) and (second_beg + 1) < len(self.second):
            if self.first[first_beg + 1] == self.second[second_beg + 1]:
                length += 1
                first_beg += 1
                second_beg += 1
            else:
                break

        return length

    def allocate_sequences(self, first_beg: int, second_beg: int):
        """
        Определяет локализацию совпадающих подпоследовательностей
        :param first_beg: Начальный индекс первого совпадения (подпоследовательности)
        :param second_beg: Начальный индекс второго совпадения (подпоследовательности)
        :return:
        """

        left_length = self._allocate_left_side(first_beg, second_beg) - 1
        right_length = self._allocate_right_side(first_beg, second_beg)

        length = left_length + right_length

        return SearchResult(
            self.first_rec,
            self.second_rec,
            length=length,
            first_beg=first_beg - left_length,
            second_beg=second_beg - left_length
        )

    @classmethod
    def distance(cls, a: List, b: List):
        """"Calculates the Levenshtein distance between a and b."""
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n, m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)  # Keep current and previous row, not entire matrix
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]
