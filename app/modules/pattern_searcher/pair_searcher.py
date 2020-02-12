import math
import random
from typing import Optional
from utils import SysMetrics
from .base import BaseSubSeqSearcher, SubSeqInfo


class PairSubSeqSearcher(BaseSubSeqSearcher):
    @SysMetrics.execution_time('Поиск наидлинейшей последовательности методом Царева')
    def tzarev(self, compare_count: int, expected_subseq_size=10 ** 5) -> Optional[SubSeqInfo]:
        """
        Поиск повторяющейся подпоследовательности с частичной
        проверкой начала и конца подпоследовательности
        :param compare_count:
        :param expected_subseq_size:
        :return:
        """

        subseq_info: Optional[SubSeqInfo] = None

        window_size = shift = int(math.sqrt(expected_subseq_size))
        while window_size >= compare_count:
            initial_shift = random.randint(1, window_size / 2)
            freq_list = self.get_freq_list(self.first, window_size, shift)
            dec_freq_list = self.get_freq_list(self.second, window_size, shift - 1, initial_shift)

            first_freq_item, second_freq_item = self.compare_freq_lists(freq_list, dec_freq_list, compare_count)

            if any((first_freq_item, second_freq_item)):
                subseq_info = self.allocate_sequences(first_freq_item.beg, second_freq_item.beg)
                break
            else:
                window_size = int(window_size / math.sqrt(2))

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

        left_length = self._allocate_left_side(first_beg, second_beg)
        right_length = self._allocate_right_side(first_beg, second_beg)

        length = left_length + right_length

        return SubSeqInfo(
            length=length,
            first_beg=first_beg - left_length,
            second_beg=second_beg - left_length
        )
