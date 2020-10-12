import csv
import pandas
import random
from logger import logger
from Bio.SeqRecord import SeqRecord
from typing import Optional, NamedTuple
from utils import GenomesReader, SequenceDispatcher
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import SubSeqInfo, PairSubSeqSearcher


class ComparedSeq(NamedTuple):
    first_seq: str
    sec_seq: str

    def check(self, first_name, second_name) -> bool:
        return (
            self.first_seq == first_name or self.sec_seq == first_name
        ) and (
            self.first_seq == second_name or self.sec_seq == second_name
        )


class Application:
    MIN_LEN = 1
    GENOMES_PATH = 'genomes/'

    def log_result(self, first_seq: SeqRecord, sec_seq: SeqRecord, expected_len: int, result: Optional[SubSeqInfo]):
        logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {sec_seq.name}')
        logger.info(f'Ожидаемая длина L = {expected_len}')

        if result:
            logger.info(f'Длина наибольш. повтора: {result.length}')
            logger.info(f'начало повтора в 1-й послед-ти: {result.first_beg}')
            logger.info(f'начало повтора во 2-й послед-ти: {result.second_beg}')
            logger.info(f'длина k: {result.k_length}')
            logger.info('##########################################################')

        else:
            logger.info(f'Подпоследовательность обнаружить не удалось')

    def search_in_pair(self, first_seq: SeqRecord, second_seq: SeqRecord,
                       expected_len, insert_seq: list, insert_tp: int) -> Optional:
        if first_seq.id != second_seq.id:
            numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
            numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
            searcher = PairSubSeqSearcher(numeric_first_seq, numeric_second_seq)
            result = searcher.tzarev(self.MIN_LEN, expected_len)
        else:
            result = None

        self.log_result(first_seq, second_seq, expected_len, result)

        return result

    def extract_seq(self, seq: SeqRecord, length: int) -> list:
        numeric = SequenceDispatcher(seq.seq).as_numeric()
        index = random.randint(0, len(numeric) - length)
        return numeric[index:index + length]

    def search_parallel(self):
        reader = GenomesReader(self.GENOMES_PATH)
        first_seq, second_seq = list(reader)[1:3]

        expected_len = 15000
        insert_length = 5000
        insert_to = random.randint(0, len(first_seq))
        extracted_seq = self.extract_seq(second_seq, insert_length)
        with open('logs/result.csv', 'w', encoding='utf-8') as result_file:
            header = [
                'Вставленная L',
                'Ожидаемая L',
                'k',
                'Найденная длина повтора',
                'Начало в 1-й послед.',
                'Начало во 2-й послед.'
            ]
            writer = csv.writer(result_file, dialect='excel')
            writer.writerow(header)
            while insert_length > 1:
                numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
                numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
                numeric_first_seq = [
                    *numeric_first_seq[0:insert_to],
                    *extracted_seq,
                    *numeric_first_seq[insert_to:len(numeric_first_seq)]
                ]

                searcher = PairSubSeqSearcher(numeric_first_seq, numeric_second_seq)
                result = searcher.tzarev(self.MIN_LEN, expected_len)
                self.log_result(first_seq, second_seq, expected_len, result)
                writer.writerow([
                    insert_length,
                    expected_len,
                    result.k_length,
                    result.length,
                    result.first_beg,
                    result.second_beg
                ])

                insert_length = int(0.9 * insert_length)
                extracted_seq = extracted_seq[0:insert_length]

        pandas_file_reader = pandas.read_csv('logs/result.csv', encoding='utf-8')
        pandas_file_reader.to_excel('logs/result.xlsx', index=None)


if __name__ == '__main__':
    Application().search_parallel()
