import csv
import pandas
from logger import logger
from typing import Optional
from utils.seq_pair import SeqPair
from Bio.SeqRecord import SeqRecord
from utils import GenomesReader, SequenceDispatcher
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import SearchResult, PairSubSeqSearcher


class Application:
    MIN_LEN = 15
    EXPECTED_LEN = 3*(10**3)
    GENOMES_PATH = '../../genomes/'

    def log_result(self, first_seq: SeqRecord, sec_seq: SeqRecord, result: Optional[SearchResult]):
        logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {sec_seq.name}')
        logger.info(f'Ожидаемая длина L = {self.EXPECTED_LEN}')

        if result:
            logger.info(f'Длина наибольш. повтора: {result.length}')
            logger.info(f'начало повтора в 1-й послед-ти: {result.first_beg}')
            logger.info(f'начало повтора во 2-й послед-ти: {result.second_beg}')
            logger.info(f'длина k: {result.k_length}')
            logger.info('##########################################################')

        else:
            logger.info(f'Подпоследовательность обнаружить не удалось')

    def search_in_pair(self, first_seq: SeqRecord, second_seq: SeqRecord) -> Optional:
        if first_seq.id != second_seq.id:
            numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
            numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
            searcher = PairSubSeqSearcher(numeric_first_seq, numeric_second_seq)
            result = searcher.tzarev(self.MIN_LEN, self.EXPECTED_LEN)
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
        seq_names = [seq.name for seq in reader]
        with ProcessPoolExecutor(max_workers=3) as pool:
            for i in range(0, len(reader)):
                for j in range(i + 1, len(reader)):
                    first_seq = reader[i]
                    second_seq = reader[j]
                    future = pool.submit(self.search_in_pair, first_seq, second_seq)
                    futures[future] = SeqPair(first_seq.name, second_seq.name)

            wait(list(futures.keys()))

        with open('logs/result.csv', 'w', encoding='utf-8') as result_file:
            header = ['-', *seq_names]
            writer = csv.DictWriter(result_file, fieldnames=header, dialect='excel')
            writer.writeheader()
            for first_seq in seq_names:
                row = {'-': first_seq}
                for second_seq in seq_names:
                    for future, compared_seq in futures.items():
                        if first_seq != second_seq and compared_seq.check(first_seq, second_seq):
                            result = future.result()
                            row.update({second_seq: str(result)})

                writer.writerow(row)
        pandas_file_reader = pandas.read_csv('results/result.csv', encoding='utf-8')
        pandas_file_reader.to_excel('results/result.xlsx', index=None)


if __name__ == '__main__':
    Application().search_parallel()
