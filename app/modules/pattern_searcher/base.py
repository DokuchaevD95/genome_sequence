import numpy as np
from typing import List, NamedTuple


class SubSeqInfo(NamedTuple):
    length: int
    first_beg: int
    second_beg: int


class BaseSubSeqSearcher:
    def __init__(self, first: List[int], second: List[int]):
        self.first = first
        self.second = second
        self.max_length = min(len(first), len(second))

    @classmethod
    def get_array(cls, seq: List[int]) -> np.ndarray:
        return np.array(seq, dtype=np.int8)
