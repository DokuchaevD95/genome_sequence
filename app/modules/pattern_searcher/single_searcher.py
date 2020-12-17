import math
import random
import numpy as np
from typing import Optional, List
from utils.sys_metrics import SysMetrics
from .base import BaseSubSeqSearcher, SearchResult
from concurrent.futures import ProcessPoolExecutor, as_completed


class SingleSubSeqSearcher(BaseSubSeqSearcher):
    """
    Класс для поиска повторяющейся
    подпоследовательности в ОДНОЙ последовательности
     """

    def __init__(self, first: List[int], second: List[int]):
        super().__init__(first, second)
        self.seq = first

    def analyse_length(self, length: int) -> Optional[SearchResult]:
        """
        Анализирует текущую длинау на полное совпадение
        :param length:
        :return:
        """

        last_seq_index = self.max_length - length
        for first_subseq_beg in range(0, last_seq_index - 1):
            for second_subseq_beg in range(first_subseq_beg + 1, last_seq_index):
                first_subseq = self.seq[first_subseq_beg: first_subseq_beg + length]
                second_subseq = self.seq[second_subseq_beg: second_subseq_beg + length]

                if np.array_equal(first_subseq, second_subseq):
                    return SearchResult(
                        self.first_rec,
                        self.second_rec,
                        length,
                        first_subseq_beg,
                        second_subseq_beg
                    )

        return None

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности BruteForce алгоритмом')
    def brute_force(self, initial_length: int = 1000) -> Optional[SearchResult]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """

        subseq_info: Optional[SearchResult] = None

        for length in range(initial_length, self.max_length - 1):
            length_info = self.analyse_length(length)
            if length_info:
                subseq_info = length_info

        return subseq_info

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности параллельным brute force')
    def parallel_brute_force(self, initial_length: int = 1000) -> Optional[SearchResult]:
        """
        Поиск повторяющейся подпоследователньности с элементами параллельности
        :return:
        """

        subseq_info: Optional[SearchResult] = None

        futures_dict = {}
        with ProcessPoolExecutor(5) as pool:
            for length in range(initial_length, self.max_length - 1):
                future = pool.submit(self.analyse_length, length)
                futures_dict[future] = future

            for future in as_completed(futures_dict.keys()):
                length = futures_dict[future]
                print(f'Computation of length = {length} is finished')
                length_info = future.result()
                if length_info:
                    subseq_info = length_info

        return subseq_info

    def _allocate_left_side(self, first_beg: int, second_beg: int) -> int:
        """Определяет длину повтора слева"""

        length = 0
        while first_beg > 0 and second_beg > 0:
            if self.seq[first_beg] == self.seq[second_beg]:
                length += 1
                first_beg -= 1
                second_beg -= 1
            else:
                break

        return length

    def _allocate_right_side(self, first_beg: int, second_beg: int) -> int:
        """Определяет длину повтора спарва"""

        length = 0
        while (first_beg + 1) < len(self.seq) and (second_beg + 1) < len(self.seq):
            if self.seq[first_beg + 1] == self.seq[second_beg + 1]:
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

        return SearchResult(
            self.first_rec,
            self.second_rec,
            length=length,
            first_beg=first_beg - left_length + 1,
            second_beg=second_beg - left_length
        )

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности методом Царева')
    def tzarev(self, compare_count: int, expected_subseq_size=10 ** 5) -> Optional[SearchResult]:
        """
        Поиск повторяющейся подпоследовательности с частичной
        проверкой начала и конца подпоследовательности
        :param compare_count:
        :param expected_subseq_size:
        :return:
        """

        subseq_info: Optional[SearchResult] = None

        window_size = shift = int(math.sqrt(expected_subseq_size))
        while window_size >= compare_count:
            initial_shift = random.randint(1, window_size / 2)
            freq_list = self.get_freq_list(self.seq, window_size, shift)
            dec_freq_list = self.get_freq_list(self.seq, window_size, shift - 1, initial_shift)

            first_freq_item, second_freq_item = self.compare_freq_lists(freq_list, dec_freq_list, compare_count)

            if any((first_freq_item, second_freq_item)):
                subseq_info = self.allocate_sequences(
                    first_freq_item.beg,
                    second_freq_item.beg
                )
                break
            else:
                window_size = int(window_size / math.sqrt(2))

        return subseq_info
