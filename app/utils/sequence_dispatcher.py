from typing import List


class SequenceDispatcher:
    _alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, seq: str):
        self.seq = seq
        self.translation = {char: self._alphabet.index(char) + 1 for char in self._alphabet}

    def as_numeric(self) -> List[int]:
        """ Метод преобразует символьную последовательность в числовую"""

        result = []
        for symbol in self.seq.lower():
            result.append(self.translation[symbol])
        return result
