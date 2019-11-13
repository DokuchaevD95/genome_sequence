import numpy as np
from typing import Optional
from utils import SysMetrics
from typing import NamedTuple


__all__ = ['HighestSubSeqInfo', 'SubSeqDispatcher']


class HighestSubSeqInfo(NamedTuple):
    length: int
    start_index: int
    repeat_start_index: int


class SubSeqDispatcher:
    def __init__(self, seq: str):
        self._seq = seq

    @property
    def array(self) -> np.ndarray:
        return np.array(list(self._seq), dtype=np.unicode)

    @SysMetrics.execution_time('поиск наидлиннейшей подпоследовательности')
    def highest_sub_seq(self) -> Optional[HighestSubSeqInfo]:
        """
        Метод ищет наидлиннейшую подпоследовательность
        прямым способом (перебором), без параллельности и пр.
        :return:
        """
        array = self.array
        min_len, max_len,  = 2, len(self._seq) - 1
        highest_sub_seq_info: Optional[HighestSubSeqInfo] = None

        for length in range(min_len, max_len):
            high_border = len(self._seq) - length
            for start_index in range(0, high_border - 1):
                for suspected_start_index in range(start_index + 1, high_border):
                    sub_sequence = array[start_index: start_index + length]
                    suspected_repeated_sub_sequence = array[suspected_start_index: suspected_start_index + length]

                    if np.array_equal(sub_sequence, suspected_repeated_sub_sequence):
                        highest_sub_seq_info = HighestSubSeqInfo(length, start_index, suspected_start_index)
                        break

                if highest_sub_seq_info and highest_sub_seq_info.length == length:
                    break

        return highest_sub_seq_info
