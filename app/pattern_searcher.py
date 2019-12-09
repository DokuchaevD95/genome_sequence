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
        self.seq_length = len(self.seq)
        self.initial_length = initial_length or 1

    @property
    def array(self) -> np.ndarray:
        return np.array(list(self.seq), dtype=np.int8)

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности')
    def brute_force(self) -> Optional[PatternInfo]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """

        array = self.array
        pattern_info: Optional[PatternInfo] = None

        for length in range(self.initial_length, self.seq_length - 1):
            high_border = len(self.seq) - length
            for start_index in range(0, high_border - 1):
                for suspected_start_index in range(start_index + 1, high_border):
                    curr_pattern = array[start_index: start_index + length]
                    suspected_pattern = array[suspected_start_index: suspected_start_index + length]

                    if np.array_equal(curr_pattern, suspected_pattern):
                        pattern_info = PatternInfo(length, start_index, suspected_start_index)
                        break

                if pattern_info and pattern_info.length == length:
                    break

        return pattern_info

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности')
    def parallel_brute_force(self) -> Optional[PatternInfo]:
        pass

    @SysMetrics.execution_time('Поиск наидлинейшей последовательности')
    def tzarev(self) -> Optional[PatternInfo]:
        pass
