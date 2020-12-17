import numpy as np
from dataclasses import dataclass
from Bio.SeqRecord import SeqRecord
from typing import List, NamedTuple, Tuple, Optional
from utils.sequence_dispatcher import SequenceDispatcher


@dataclass
class SearchResult:
    first_rec: SeqRecord
    second_rec: SeqRecord
    length: int
    first_beg: int
    second_beg: int
    k_length: int = None

    @property
    def repeat_str(self) -> str:
        return self.first_rec.seq[self.first_beg:self.first_beg + self.length]

    def __str__(self) -> str:
        return f'Длина повтора: {self.length}\n' \
               f'Начало повтора в 1-й пос-ти: {self.first_beg}\n' \
               f'Начало повтора во 2-й пос-ти: {self.second_beg}\n' \
               f'Длина k: {self.k_length}'


class FreqItem(NamedTuple):
    beg: int
    slice_: List[int]


class BaseSubSeqSearcher:
    def __init__(self, first_rec: SeqRecord, second_rec: SeqRecord):
        self.first_rec = first_rec
        self.second_rec = second_rec
        self.first = SequenceDispatcher(first_rec.seq).as_numeric()
        self.second = SequenceDispatcher(second_rec.seq).as_numeric()
        self.max_length = min(len(self.first), len(self.second))

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
            if end <= len(seq):
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
                if first_item.slice_[0: compare_count] != second_item.slice_[0: compare_count]:
                    continue
                elif first_item.slice_ == second_item.slice_:
                    first_freq_item = first_item
                    second_freq_item = second_item
                    break
                else:
                    continue

        return first_freq_item, second_freq_item

    @staticmethod
    def get_repeat_count(first_list: List[FreqItem],
                           second_list: List[FreqItem],
                           compare_count: int = None) -> int:
        """
        Количество повторов определенной длины k
        :param first_list:
        :param second_list:
        :param compare_count:
        :return:
        """

        count = 0
        for first_item in first_list:
            for second_item in second_list:
                if first_item.slice_[0: compare_count] != second_item.slice_[0: compare_count]:
                    continue
                elif first_item.slice_ == second_item.slice_:
                    count += 1
                else:
                    continue

        return count
