import os
import csv

from utils.seq_pair import SeqPair
from Bio.SeqRecord import SeqRecord
from typing import Dict, Optional, List
from modules.pattern_searcher import SearchResult


class ResultsRW:
    _DIR_NAME = 'results/'

    @classmethod
    def read(cls, genomes: List[SeqRecord], filename: str) -> Optional[Dict[SeqPair, SearchResult]]:
        filepath = f'{cls._DIR_NAME}/{filename}'
        if os.path.exists(filepath):
            results = {}
            with open(filepath, 'r') as file:
                csv_reader = csv.reader(file, dialect='excel')
                for row in csv_reader:
                    pair = SeqPair(
                        row[0],
                        row[1]
                    )
                    info = SearchResult(
                        first_rec=cls.get_rec_by_name(genomes, row[0]),
                        second_rec=cls.get_rec_by_name(genomes, row[1]),
                        first_beg=int(row[2]),
                        second_beg=int(row[3]),
                        length=int(row[4])
                    )
                    results[pair] = info
        else:
            results = None
        return results

    @classmethod
    def write(cls, results: Dict[SeqPair, SearchResult], filename: str):
        with open(f'{cls._DIR_NAME}/{filename}', 'w') as file:
            csv_writer = csv.writer(file, dialect='excel')
            for pair, info in results.items():
                csv_writer.writerow([
                    pair.first_seq,
                    pair.sec_seq,
                    info.first_beg,
                    info.second_beg,
                    info.length
                ])

    @staticmethod
    def get_rec_by_name(genomes: List[SeqRecord], name: str) -> SeqRecord:
        result = None
        for rec in genomes:
            if rec.name == name:
                result = rec
                break
        return result
