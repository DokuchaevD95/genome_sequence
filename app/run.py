from logger import logger
from utils import GenomesReader, SequenceDispatcher
from pattern_searcher import PatterSearcher, PatternInfo


def main():
    logger.debug('Process was started')
    reader = GenomesReader('genomes/')

    for sequence in reader:
        logger.info(f'Исследование последовательности: {sequence.name}')
        numeric_seq = SequenceDispatcher(sequence.seq).as_numeric()
        dispatcher = PatterSearcher(numeric_seq)
        result: PatternInfo = dispatcher.tzarev(30)

        if result:
            logger.info(f'Наибольшая подпоследовательность длиной {result.length}'
                        f'последовательность начинается с индекса №{result.first_subseq_beg_index}'
                        f'повтор начинается с индекса №{result.second_subseq_beg_index}')

    logger.debug('Process was done')


if __name__ == '__main__':
    main()
