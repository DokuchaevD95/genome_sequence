import csv
import math
import pandas

from typing import List
from logger import logger
from Bio.SeqRecord import SeqRecord
from typing import Optional, NamedTuple
from utils.dict_generator import DictGenerator
from utils import GenomesReader, SequenceDispatcher
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import (
    SubSeqInfo,
    BrutePairSearcher
)


class SeqPair(NamedTuple):
    first_seq: str
    sec_seq: str

    def check(self, first_name, second_name) -> bool:
        return (
            self.first_seq == first_name or self.sec_seq == first_name
        ) and (
            self.first_seq == second_name or self.sec_seq == second_name
        )

    def __repr__(self):
        return f'{self.first_seq} / {self.sec_seq}'


class Application:
    ALPHABET = ['A', 'C', 'G', 'T']
    GENOMES_PATH = 'genomes/'

    def log_result(self, first_seq: SeqRecord, sec_seq: SeqRecord, result: Optional[SubSeqInfo]):
        logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {sec_seq.name}')
        if result:
            logger.info(f'Длина наибольш. повтора: {result.length}')
            logger.info(f'начало повтора в 1-й послед-ти: {result.first_beg}')
            logger.info(f'начало повтора во 2-й послед-ти: {result.second_beg}')
            logger.info('##########################################################')
        else:
            logger.info(f'Подпоследовательность обнаружить не удалось')

    def search_in_pair(self, first_seq: SeqRecord, second_seq: SeqRecord) -> Optional:
        if first_seq.id != second_seq.id:
            numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
            numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
            searcher = BrutePairSearcher(numeric_first_seq, numeric_second_seq)
            result = searcher.search()
        else:
            result = None

        self.log_result(first_seq, second_seq, result)

        return result

    def search(self):
        reader = GenomesReader(self.GENOMES_PATH)
        for first_seq in reader:
            for second_seq in reader:
                self.search_in_pair(first_seq, second_seq)

    def search_parallel(self):
        futures = {}
        reader = GenomesReader(self.GENOMES_PATH)
        reader = list(reader)[0:2]

        with ProcessPoolExecutor(max_workers=3) as pool:
            for i in range(0, len(reader)):
                for j in range(i + 1, len(reader)):
                    first_seq = reader[i]
                    second_seq = reader[j]
                    future = pool.submit(self.search_in_pair, first_seq, second_seq)
                    futures[future] = SeqPair(first_seq.name, second_seq.name)

            wait(list(futures.keys()))

        self.analyze(1, reader, futures)
        self.analyze(2, reader, futures)
        self.analyze(3, reader, futures)

    @staticmethod
    def calc_freq(combinations: List[str], repeat: str):
        count = dict.fromkeys(combinations, 0)
        repeat = repeat.upper()
        for comb in combinations:
            count[comb] = repeat.count(comb)
        return count

    @staticmethod
    def calc_distance(combinations: list, x_freq: dict, y_freq: dict) -> float:
        total_sum = 0
        for comb in combinations:
            total_sum += (x_freq[comb] - y_freq[comb]) ** 2
        return math.sqrt(total_sum)

    def analyze(self, freq_len: int, genomes: List[SeqRecord], futures: dict):
        dg = DictGenerator(self.ALPHABET)
        combinations = dg.generate(freq_len)
        pair_freq = {}
        for first in genomes:
            for second in genomes:
                for future, pair in futures.items():
                    if first.name != second.name and pair.check(first.name, second.name):
                        result = future.result()
                        repeat = first.seq[result.first_beg:result.first_beg + result.length]
                        repeat_freq = self.calc_freq(combinations, repeat)
                        pair_freq[pair] = repeat_freq

        self.export_result(pair_freq)

    def export_result(self, pair_freq: dict):
        with open('logs/result.csv', 'w', encoding='utf-8') as result_file:
            pair_names = [str(pair) for pair in pair_freq]
            header = ['-', *pair_names]
            writer = csv.DictWriter(result_file, fieldnames=header, dialect='excel')
            writer.writeheader()
            for first_pair in pair_freq:
                row = {'-': first_seq}
                for second_seq in seq_names:
                    for future, compared_seq in futures.items():
                        if first_seq != second_seq and compared_seq.check(first_seq, second_seq):
                            result = future.result()
                            row.update({second_seq: str(result)})

                writer.writerow(row)
        pandas_file_reader = pandas.read_csv('logs/result.csv', encoding='utf-8')
        pandas_file_reader.to_excel('logs/result.xlsx', index=None


if __name__ == '__main__':
    Application().search_parallel()
