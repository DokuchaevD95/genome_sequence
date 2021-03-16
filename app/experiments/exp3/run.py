import csv
import math
import pandas

from typing import List
from logger import logger
from utils import GenomesReader
from typing import Optional, Dict
from utils.seq_pair import SeqPair
from Bio.SeqRecord import SeqRecord
from utils.results_rw import ResultsRW
from utils.dict_generator import DictGenerator
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import (
    SearchResult,
    BrutePairSearcher
)


class Application:
    ALPHABET = ['A', 'C', 'G', 'T']
    GENOMES_PATH = '../../genomes/'

    def log_result(self, first_seq: SeqRecord, sec_seq: SeqRecord, result: Optional[SearchResult]):
        logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {sec_seq.name}')
        if result:
            logger.info(f'Длина наибольш. повтора: {result.length}')
            logger.info(f'начало повтора в 1-й послед-ти: {result.first_beg}')
            logger.info(f'начало повтора во 2-й послед-ти: {result.second_beg}')
            logger.info('##########################################################')
        else:
            logger.info(f'Подпоследовательность обнаружить не удалось')

    def search_in_pair(self, first_rec: SeqRecord, second_rec: SeqRecord) -> Optional:
        if first_rec.id != second_rec.id:
            searcher = BrutePairSearcher(first_rec, second_rec)
            result = searcher.search()
        else:
            result = None

        self.log_result(first_rec, second_rec, result)

        return result

    def search_parallel(self):
        reader = GenomesReader(self.GENOMES_PATH)
        genomes = list(reader)

        search_results = self.find_repeats(genomes)
        self.export_result('distance1', self.analyze(1, genomes, search_results))
        self.export_result('distance2', self.analyze(2, genomes, search_results))
        self.export_result('distance3', self.analyze(3, genomes, search_results))

    def find_repeats(self, genomes: list) -> dict:
        if not (search_results := ResultsRW.read(genomes, 'brute_searching.csv')):
            search_results = {}
            with ProcessPoolExecutor() as pool:
                for i in range(0, len(genomes)):
                    for j in range(i + 1, len(genomes)):
                        first_seq = genomes[i]
                        second_seq = genomes[j]
                        future = pool.submit(self.search_in_pair, first_seq, second_seq)
                        pair = SeqPair(first_seq.name, second_seq.name)
                        search_results[pair] = future
                wait(list(search_results.values()))
                search_results = {pair: future.result() for pair, future in search_results.items()}
            ResultsRW.write(search_results, 'brute_searching.csv')

        return search_results

    @staticmethod
    def calc_freq(freq_len: int, combinations: List[str], repeat: str):
        count = dict.fromkeys(combinations, 0)
        normalization = len(repeat) - (freq_len - 1)
        repeat = repeat.upper()
        for comb in combinations:
            for index in range(freq_len, len(repeat)):
                repeat_comb = repeat[index - freq_len:index]
                if repeat_comb == comb:
                    count[comb] += 1
            count[comb] /= normalization
        return count

    @staticmethod
    def calc_distance(x_freq: dict, y_freq: dict) -> float:
        total_sum = 0
        combinations = list(x_freq)
        for comb in combinations:
            total_sum += (x_freq[comb] - y_freq[comb]) ** 2
        return math.sqrt(total_sum)

    def analyze(self, freq_len: int, genomes: List[SeqRecord], search_results: dict):
        dg = DictGenerator(self.ALPHABET)
        combinations = dg.generate(freq_len)
        pair_freq = {}
        for first in genomes:
            for second in genomes:
                for pair, result in search_results.items():
                    if first.name != second.name and pair.check(first.name, second.name):
                        repeat = result.repeat_str
                        repeat_freq = self.calc_freq(freq_len, combinations, repeat)
                        pair_freq[pair] = repeat_freq

        return pair_freq

    def export_result(self, filename: str, freq_analysis_results: dict):
        with open(f'logs/{filename}.csv', 'w', encoding='utf-8') as result_file:
            pair_names = [str(pair) for pair in freq_analysis_results]
            header = ['-', *pair_names]
            writer = csv.DictWriter(result_file, fieldnames=header, dialect='excel')
            writer.writeheader()
            for col_pair, col_freq in freq_analysis_results.items():
                row = {'-': str(col_pair)}
                for row_pair, row_freq in freq_analysis_results.items():
                    if col_pair != row_pair:
                        row.update({str(row_pair): self.calc_distance(col_freq, row_freq)})
                    else:
                        row.update({str(row_pair): 0})

                writer.writerow(row)
        pandas_file_reader = pandas.read_csv(f'results/{filename}.csv', encoding='utf-8')
        pandas_file_reader.to_excel(f'results/{filename}.xlsx', index=None)


if __name__ == '__main__':
    Application().search_parallel()


