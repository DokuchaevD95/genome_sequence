import numpy as np
from typing import List, NamedTuple, Tuple, Optional


class SubSeqInfo(NamedTuple):
    length: int
    first_beg: int
    second_beg: int


class FreqItem(NamedTuple):
    beg: int
    slice_: List[int]


class BaseSubSeqSearcher:
    def __init__(self, first: List[int], second: List[int]):
        self.first = first
        self.second = second
        self.max_length = min(len(first), len(second))

    @classmethod
    def get_array(cls, seq: List[int]) -> np.ndarray:
        return np.array(seq, dtype=np.int8)

    @classmethod
    def get_freq_list(cls, seq: List[int], size: int, shift: int, initial_shift: int = 0) -> List[FreqItem]:
        """
        Нарезает последжовательность на подпоследователдьности
        длины size со смещением shift
        :param seq:
        :param size:
        :param shift:
        :param initial_shift:
        :return:
        """
        result = []
        for beg in range(0 + initial_shift, len(seq), shift):
            end = beg + size
            item = FreqItem(beg, seq[beg: end])
            result.append(item)
        return result

    @staticmethod
    def compare_freq_lists(first_list: List[FreqItem],
                           second_list: List[FreqItem],
                           compare_count: int = None) -> Tuple[Optional[FreqItem], Optional[FreqItem]]:
        """
        Ищет в первом массиве такую подпоследовательность, которая
        входит во второй массив с подпоследовательностями
        :param first_list:
        :param second_list:
        :param compare_count:
        :return:
        """

        first_freq_item, second_freq_item = None, None
        for first_item in first_list:
            for second_item in second_list:
                if first_item.slice_[0: compare_count] == second_item.slice_[0: compare_count]:
                    first_freq_item = first_item
                    second_freq_item = second_item
                    break

        return first_freq_item, second_freq_item
