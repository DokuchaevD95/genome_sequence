import copy
from collections import Counter


__all__ = ['SequenceValidator']


class SequenceValidator:
    __alphabet: set = {'a', 'c', 'g', 't'}
    """Класс для проверки на отсутсвие лишних символов в последовательнности"""

    @property
    def alphabet(self) -> set:
        return copy.copy(self.__alphabet)

    @classmethod
    def validate(cls, genome_sequence: str) -> bool:
        counter = Counter(genome_sequence.lower())
        alphabet_diff = cls.__alphabet.difference(counter.keys())
        return bool(alphabet_diff)


# TODO: Реализовать логгирование количества символов в последовательности
