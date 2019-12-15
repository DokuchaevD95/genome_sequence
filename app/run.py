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
        result: PatternInfo = dispatcher.parallel_brute_force()

        if result:
            logger.info(f'Наибольшая подпоследовательность длиной {result.length}'
                        f'последовательность начинается с индекса №{result.start_index}'
                        f'первый повтор начинается с индекса №{result.repeat_start_index}')

    logger.debug('Process was done')


if __name__ == '__main__':
    main()
