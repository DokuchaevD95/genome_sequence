from typing import List


class SequenceDispatcher:
    __translation = {
        'a': 1,
        'c': 2,
        'g': 3,
        't': 4,
        'n': 5,
        'y': 6
    }

    def __init__(self, seq: str):
        self.seq = seq

    def as_numeric(self) -> List[int]:
        """ Метод преобразует символьную последовательность в числовую"""

        result = []
        for symbol in self.seq.lower():
            result.append(self.__translation[symbol])
        return result
