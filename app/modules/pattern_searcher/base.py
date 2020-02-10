import numpy as np
from typing import List, NamedTuple


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
