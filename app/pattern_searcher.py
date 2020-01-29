import math
import numpy as np
from utils import SysMetrics
from typing import Optional, List, NamedTuple, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


__all__ = ['PatternInfo', 'PatterSearcher']


class PatternInfo(NamedTuple):
    length: int
    first_subseq_beg_index: int
    second_subseq_beg_index: int


class PatterSearcher:
    THREADS = 5

    def __init__(self, numeric_seq: List[int], initial_length: Optional[int] = 2000000):
        self.seq = numeric_seq
        self.array = self.get_array()
        self.seq_length = len(self.seq)
        self.initial_length = initial_length or 1

    def get_array(self) -> np.ndarray:
        return np.array(list(self.seq), dtype=np.int8)

    def sort_out_length(self, length: int) -> Optional[PatternInfo]:
        """
        Анализирует текущую длинау на полное совпадение
        :param length:
        :return:
        """

        last_seq_index = self.seq_length - length
        for first_seq_start_index in range(0, last_seq_index - 1):
            for second_seq_start_index in range(first_seq_start_index + 1, last_seq_index):
                first_seq = self.array[first_seq_start_index: first_seq_start_index + length]
                second_seq = self.array[second_seq_start_index: second_seq_start_index + length]

                if np.array_equal(first_seq, second_seq):
                    return PatternInfo(length, first_seq_start_index, second_seq_start_index)

        return None

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности brute force алгоритмом')
    def brute_force(self) -> Optional[PatternInfo]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """

        pattern_info: Optional[PatternInfo] = None

        for length in range(self.initial_length, self.seq_length - 1):
            length_info = self.sort_out_length(length)
            if length_info:
                pattern_info = length_info

        return pattern_info

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности параллельным brute force')
    def parallel_brute_force(self) -> Optional[PatternInfo]:
        """
        Поиск повторяющейся подпоследователньности с элементами параллельности
        :return:
        """

        pattern_info: Optional[PatternInfo] = None

        futures_dict = {}
        with ProcessPoolExecutor(5) as pool:
            for length in range(self.initial_length, self.seq_length - 1):
                future = pool.submit(self.sort_out_length(), length)
                futures_dict[future] = future

            for future in as_completed(futures_dict.keys()):
                length = futures_dict[future]
                print(f'Computation of length = {length} is finished')
                length_info = future.result()
                if length_info:
                    pattern_info = length_info

        return pattern_info

    # def sort_out_length_partially(self, length: int, part_length: int) -> Optional[PatternInfo]:
    #     """
    #     Анализирует текущую длинау на ЧАСТИЧНОЕ совпадение по первым и последним символам
    #     :param length:
    #     :param part_length:
    #     :return:
    #     """
    #
    #     last_seq_index = self.seq_length - length
    #     for first_seq_start_index in range(0, last_seq_index - 1):
    #         for second_seq_start_index in range(first_seq_start_index + 1, last_seq_index):
    #             first_seq_beg = self.array[first_seq_start_index: part_length]
    #             second_seq_beg = self.array[second_seq_start_index: second_seq_start_index + part_length]
    #
    #             if np.array_equal(first_seq_beg, second_seq_beg):
    #                 return PatternInfo(length, first_seq_start_index, second_seq_start_index)
    #
    #     return None

    # @SysMetrics.execution_time('Поиск наидлинейшей последовательности параллельным методом Царева')
    # def tzarev_parallel(self, part_length: int) -> Optional[PatternInfo]:
    #     """
    #     Поиск повторяющейся подпоследователньности с элементами параллельности
    #     :return:
    #     """
    #
    #     pattern_info: Optional[PatternInfo] = None
    #
    #     futures_dict = {}
    #     with ProcessPoolExecutor(5) as pool:
    #         for length in range(self.initial_length, self.seq_length - 1):
    #             future = pool.submit(self.sort_out_length_partially(length, part_length)
    #             futures_dict[future] = future
    #
    #         for future in as_completed(futures_dict.keys()):
    #             length = futures_dict[future]
    #             print(f'Computation of length = {length} is finished')
    #             length_info = future.result()
    #             if length_info:
    #                 pattern_info = length_info
    #
    #     return pattern_info

    def get_frequency_list(self, size: int, shift: int):
        """
        Нарезает последжовательность на подпоследователдьности
        длины size со смещением shift
        :param size:
        :param shift:
        :return:
        """
        result = []
        for beg in range(0, self.seq_length, shift):
            end = beg + size
            result.append(self.seq[beg: end])
        return result

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
        while (first_end + 1) <= self.seq_length and (second_end + 1) <= self.seq_length:
            if self.seq[first_end + 1] == self.seq[second_end + 1]:
                length += 1
                first_end += 1
                second_end += 1
            else:
                break

        return PatternInfo(
            length=length,
            first_subseq_beg_index=first_beg,
            second_subseq_beg_index=second_beg
        )

    @staticmethod
    def compare_frequencies_list(freq_list: list, decremented_freq_list: list) -> tuple:
        """
        Ищет в первом массиве такую подпоследовательность, которая
        входит во второй массив с подпоследовательностями
        :param freq_list:
        :param decremented_freq_list:
        :return:
        """
        freq_list_index, decremented_freq_list_index = None, None
        for index, value in enumerate(freq_list):
            try:
                decremented_freq_list_index = decremented_freq_list.index(value)
                freq_list_index = index
                break
            except ValueError:
                pass

        return freq_list_index, decremented_freq_list_index


    @SysMetrics.execution_time('Поиск наидлинейшей последовательности методом Царева')
    def tzarev(self, part_length: int, expected_pattern_size=10**5) -> Optional[PatternInfo]:
        """
        Поиск повторяющейся подпоследовательности с частичной
        проверкой начала и конца подпоследовательности
        :param part_length:
        :param expected_pattern_size:
        :return:
        """

        pattern_info: Optional[PatternInfo] = None

        window_size = int(math.sqrt(expected_pattern_size))
        while window_size > 1:
            freq_list = self.get_frequency_list(window_size, window_size)
            decremented_freq_list = self.get_frequency_list(window_size, window_size-1)[1:]

            first_subseq_index, second_subseq_index = self.compare_frequencies_list(freq_list, decremented_freq_list)

            if any((first_subseq_index, second_subseq_index)):
                first_subseq_index *= window_size
                second_subseq_index *= (window_size - 1)
                pattern_info = self.allocate_sequences(first_subseq_index, second_subseq_index, window_size)
            else:
                window_size = int(window_size / math.sqrt(2))

        return pattern_info
