from logger import logger
from utils import GenomesReader, SequenceDispatcher
from modules.pattern_searcher import SubSeqSearcherFabric


def search_in_pairs():
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
