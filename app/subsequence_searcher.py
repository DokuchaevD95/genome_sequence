from utils import SysMetrics
from typing import NamedTuple


__all__ = ['HighestSubSeqInfo', 'SubSeqSearcher']


class HighestSubSeqInfo(NamedTuple):
    start_index: int
    length: int


class SubSeqSearcher:
    def __init__(self, seq: str):
        self._seq = seq

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности')
    def highest_sub_seq(self) -> HighestSubSeqInfo:
        pass
