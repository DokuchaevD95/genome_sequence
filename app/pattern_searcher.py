import numpy as np
from utils import SysMetrics
from typing import NamedTuple
from typing import Optional, List


__all__ = ['PatternInfo', 'PatterSearcher']


class PatternInfo(NamedTuple):
    length: int
    start_index: int
    repeat_start_index: int


class PatterSearcher:
    def __init__(self, numeric_seq: List[int], initial_length: Optional[int] = 1000):
        self.seq = numeric_seq
        self.array = self.get_array()
        self.seq_length = len(self.seq)
        self.initial_length = initial_length or 1

    def get_array(self) -> np.ndarray:
        return np.array(list(self.seq), dtype=np.int8)

    def check_length(self, length: int) -> Optional[PatternInfo]:
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

    def check_length_partially(self, length: int, part_length: int) -> Optional[PatternInfo]:
        """
        Анализирует текущую длинау на ЧАСТИЧНОЕ совпадение по первым и последним символам
        :param length:
        :param part_length:
        :return:
        """

        last_seq_index = self.seq_length - length
        for first_seq_start_index in range(0, last_seq_index - 1):
            for second_seq_start_index in range(first_seq_start_index + 1, last_seq_index):
                first_seq_last_index = first_seq_start_index + length
                second_seq_last_index = second_seq_start_index + length

                first_seq_beg = self.array[first_seq_start_index: part_length]
                first_seq_end = self.array[first_seq_last_index - part_length: first_seq_last_index]

                second_seq_beg = self.array[second_seq_start_index: second_seq_start_index + part_length]
                second_seq_end = self.array[second_seq_last_index - part_length: second_seq_last_index]

                if np.array_equal(first_seq_beg, second_seq_beg) and np.array_equal(first_seq_end, second_seq_end):
                    return PatternInfo(length, first_seq_start_index, second_seq_start_index)

        return None

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности')
    def brute_force(self) -> Optional[PatternInfo]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """

        pattern_info: Optional[PatternInfo] = None

        for length in range(self.initial_length, self.seq_length - 1):
            length_info = self.check_length(length)

            if length_info:
                pattern_info = length_info

        return pattern_info

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности')
    def parallel_brute_force(self) -> Optional[PatternInfo]:
        pass

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности')
    def tzarev(self) -> Optional[PatternInfo]:
        pass
