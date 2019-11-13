import os
from Bio import SeqIO
from typing import List


__all__ = ['GenomesReader']


class GenomesReader:
    _FORMAT = 'fasta'
    _EXTENSION = '.fasta'

    def __init__(self, dir_path: str):
        self._dir_path = dir_path
        self._dir_content: List[str] = os.listdir(dir_path)
        self._dir_content = list(filter(lambda x: x.endswith(self._EXTENSION), self._dir_content))
        if not self._dir_content:
            message = f'В директории {dir_path} не найдено геномов с расширением {self._EXTENSION}'
            raise FileNotFoundError(message)

    def __iter__(self):
        for filename in self._dir_content:
            relative_path = os.path.join(self._dir_path, filename)
            with open(relative_path, 'r') as file:
                seq_generator = SeqIO.parse(file, self._FORMAT)
                for seq in seq_generator:
                    yield seq

