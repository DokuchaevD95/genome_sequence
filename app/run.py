from logger import logger
from utils import GenomesReader, SequenceDispatcher
from modules.pattern_searcher import SubSeqSearcherFabric


def search_in_pairs():
    reader = GenomesReader('genomes/')
    expected_length = 10**5
    for first_seq in reader:
        for second_seq in reader:
            if first_seq.id != second_seq.id:
                logger.info(f'Поиск наидлинейшей общей подпос-ти в {first_seq.name} и {second_seq.name}')
                logger.info(f'Ожидаемая длина L = expected_length')
                numeric_first_seq = SequenceDispatcher(first_seq.seq).as_numeric()
                numeric_second_seq = SequenceDispatcher(second_seq.seq).as_numeric()
                searcher = SubSeqSearcherFabric.get_searcher(numeric_first_seq, numeric_second_seq)
                result = searcher.tzarev(30, expected_length)

                if result:
                    logger.info(f'Наибольшая подпоследовательность длиной: {result.length}')
                    logger.info(f'начало подпос-ти в 1-й послед-ти: {result.first_beg}')
                    logger.info(f'начало подпос-ти во 2-й послед-ти: {result.second_beg}')


def search_in_each_self():
    reader = GenomesReader('genomes/')
    for sequence in reader:
        logger.info(f'Исследование последовательности: {sequence.name}')
        numeric_seq = SequenceDispatcher(sequence.seq).as_numeric()
        searcher = SubSeqSearcherFabric.get_searcher(numeric_seq, numeric_seq)
        result = searcher.tzarev(30)

        if result:
            logger.info(f'Наибольшая подпоследовательность длиной {result.length}')
            logger.info(f'последовательность начинается с индекса {result.first_beg}')
            logger.info(f'повтор начинается с индекса {result.second_beg}')


def main():
    search_in_pairs()


if __name__ == '__main__':
    main()
