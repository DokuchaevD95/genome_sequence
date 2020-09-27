import os
from Bio import SeqIO
from typing import List
from config import config
from Bio.SeqIO import SeqRecord


__all__ = ['GenomesReader']


class GenomesReader:
    _FORMAT = config['genome_format']

    def __init__(self, dir_path: str):
        self._dir_path = dir_path
        self._dir_content: List[str] = os.listdir(dir_path)

    def __iter__(self) -> SeqRecord:
        for filename in self._dir_content:
            relative_path = os.path.join(self._dir_path, filename)
            with open(relative_path, 'r') as file:
                if config['genome_list']:
                    for genome in SeqIO.parse(file, config['genome_format']):
                        yield genome
                else:
                    yield SeqIO.read(file, config['genome_format'])
