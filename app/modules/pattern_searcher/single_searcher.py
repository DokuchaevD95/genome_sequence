import math
import random
import numpy as np
from logger import logger
from typing import Optional, List, Tuple
from utils.sys_metrics import SysMetrics
from .base import BaseSubSeqSearcher, SubSeqInfo
from concurrent.futures import ProcessPoolExecutor, as_completed


class SingleSubSeqSearcher(BaseSubSeqSearcher):
    """
    Класс для поиска повторяющейся
    подпоследовательности в ОДНОЙ последовательности
     """
    def __init__(self, first: List[int], second: List[int]):
        super().__init__(first, second)
        self.seq = first

    def analyse_length(self, length: int) -> Optional[SubSeqInfo]:
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
                    return SubSeqInfo(length, first_subseq_beg, second_subseq_beg)

        return None

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности BruteForce алгоритмом')
    def brute_force(self, initial_length: int = 1000) -> Optional[SubSeqInfo]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """

        subseq_info: Optional[SubSeqInfo] = None

        for length in range(initial_length, self.max_length - 1):
            length_info = self.analyse_length(length)
            if length_info:
                subseq_info = length_info

        return subseq_info

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности параллельным brute force')
    def parallel_brute_force(self, initial_length: int = 1000) -> Optional[SubSeqInfo]:
        """
        Поиск повторяющейся подпоследователньности с элементами параллельности
        :return:
        """

        subseq_info: Optional[SubSeqInfo] = None

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

    def allocate_sequences(self, first_subseq_index: int, second_subseq_index: int, window_size: int):
        """
        Определяет локализацию совпадающих подпоследовательностей
        :param first_subseq_index: Начальный индекс первого совпадения (подпоследовательности)
        :param second_subseq_index: Начальный индекс второго совпадения (подпоследовательности)
        :param window_size: размер окна
        :return:
        """
        length = window_size

        # Локализация левой стороны
        first_beg = first_subseq_index
        second_beg = second_subseq_index
        while (first_beg - 1) > 0 and (second_beg - 1) > 0:
            if self.seq[first_beg - 1] == self.seq[second_beg - 1]:
                length += 1
                first_beg -= 1
                second_beg -= 1
            else:
                break

        # Локализация правой стороны
        first_end = first_subseq_index + window_size
        second_end = second_subseq_index + window_size
        while (first_end + 1) < self.max_length and (second_end + 1) < self.max_length:
            if self.seq[first_end + 1] == self.seq[second_end + 1]:
                length += 1
                first_end += 1
                second_end += 1
            else:
                break

        return SubSeqInfo(
            length=length,
            first_beg=first_beg,
            second_beg=second_beg
        )

    @staticmethod
    def compare_freq_lists(freq_list: list, dec_freq_list: list) -> Tuple[Optional[int], Optional[int]]:
        """
        Ищет в первом массиве такую подпоследовательность, которая
        входит во второй массив с подпоследовательностями
        :param freq_list:
        :param dec_freq_list:
        :return:
        """
        freq_list_index, dec_freq_list_index = None, None
        for index, value in enumerate(freq_list):
            try:
                dec_freq_list_index = dec_freq_list.index(value)
                freq_list_index = index
                break
            except ValueError:
                pass

        return freq_list_index, dec_freq_list_index

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности методом Царева')
    def tzarev(self, part_length: int, expected_pattern_size=10**5) -> Optional[SubSeqInfo]:
        """
        Поиск повторяющейся подпоследовательности с частичной
        проверкой начала и конца подпоследовательности
        :param part_length:
        :param expected_pattern_size:
        :return:
        """

        subseq_info: Optional[SubSeqInfo] = None

        window_size = shift = int(math.sqrt(expected_pattern_size))
        while window_size > 1:
            initial_shift = random.randint(1, window_size / 2)
            logger.info(f'Current window_size = {window_size}')
            logger.info(f'Current initial_shift = {initial_shift}')
            freq_list = self.get_freq_list(self.seq, window_size, shift)
            dec_freq_list = self.get_freq_list(self.seq, window_size, shift-1, initial_shift)

            first_subseq_index, second_subseq_index = self.compare_freq_lists(freq_list, dec_freq_list)

            if any((first_subseq_index, second_subseq_index)):
                first_subseq_index *= shift
                second_subseq_index *= (shift - 1)
                second_subseq_index += initial_shift
                subseq_info = self.allocate_sequences(first_subseq_index, second_subseq_index, window_size)
                break
            else:
                window_size = int(window_size / math.sqrt(2))

        return subseq_info
