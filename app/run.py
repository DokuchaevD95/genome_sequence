import csv
from logger import logger
from Bio.SeqRecord import SeqRecord
from typing import Optional, NamedTuple
from utils import GenomesReader, SequenceDispatcher
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import SubSeqSearcherFabric, SubSeqInfo


class ComparedSeq(NamedTuple):
    first_seq: str
    sec_seq: str


class Application:
    EXPECTED_TIME = 10**5
    GENOMES_PATH = 'genomes/'

    def log_result(self, first_seq: SeqRecord, sec_seq: SeqRecord, result: Optional[SubSeqInfo]):
        logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {sec_seq.name}')
        logger.info(f'Ожидаемая длина L = {self.EXPECTED_TIME}')

        if result:
            logger.info(f'Наибольшая подпоследовательность длиной: {result.length}')
            logger.info(f'начало подпос-ти в 1-й послед-ти: {result.first_beg}')
            logger.info(f'начало подпос-ти во 2-й послед-ти: {result.second_beg}')
            logger.info('##########################################################')

        else:
            logger.info(f'Подпоследовательность обнаружить не удалось')

    def search_in_pair(self, first_seq: SeqRecord, second_seq: SeqRecord) -> Optional:
        if first_seq.id != second_seq.id:
            numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
            numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
            searcher = SubSeqSearcherFabric.get_searcher(numeric_first_seq, numeric_second_seq)
            result = searcher.tzarev(20, self.EXPECTED_TIME)
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
        seq_names = [seq.name for seq in reader]
        with ProcessPoolExecutor(max_workers=4) as pool:
            for first_seq in reader:
                for second_seq in reader:
                    future = pool.submit(self.search_in_pair, first_seq, second_seq)
                    futures[future] = ComparedSeq(first_seq.name, second_seq.name)

            wait(list(futures.keys()))

        with open('logs/result.csv', 'w') as result_file:
            header = ['-', *seq_names]
            writer = csv.DictWriter(result_file, fieldnames=header)
            writer.writeheader()
            for first_seq in seq_names:
                row = {'-': first_seq}
                for second_seq in seq_names:
                    for future, compared_seq in futures.items():
                        if compared_seq.first_seq == first_seq and compared_seq.sec_seq == second_seq:
                            result = future.result()
                            row.update({second_seq: str(result)})

                writer.writerow(row)


if __name__ == '__main__':
    Application().search_parallel()
