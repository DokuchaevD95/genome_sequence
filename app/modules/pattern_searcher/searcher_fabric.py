from typing import List
from .duo_searcher import DuoSubSeqSearcher
from .single_searcher import SingleSubSeqSearcher


class SubSeqSearcherFabric:
    @classmethod
    def get_searcher(cls, first: List[int], second: List[int]):
        if first == second:
            return SingleSubSeqSearcher(first, second)
        else:
            return DuoSubSeqSearcher(first, second)
