from logger import logger
from utils import GenomesReader, SequenceDispatcher
from modules.pattern_searcher import SubSeqSearcherFabric


def main():
    logger.debug('Process was started')
    reader = GenomesReader('genomes/')

    for sequence in reader:
        logger.info(f'Исследование последовательности: {sequence.name}')
        numeric_seq = SequenceDispatcher(sequence.seq).as_numeric()
        searcher = SubSeqSearcherFabric.get_searcher(numeric_seq, numeric_seq)
        result = searcher.tzarev(30)

        if result:
            logger.info(f'Наибольшая подпоследовательность длиной {result.length}'
                        f'последовательность начинается с индекса №{result.first_beg}'
                        f'повтор начинается с индекса №{result.second_beg}')

    logger.debug('Process was done')


if __name__ == '__main__':
    main()
