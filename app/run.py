from logger import logger
from utils import GenomesReader
from sub_seq_dispatcher import SubSeqDispatcher, HighestSubSeqInfo


def main():
    logger.debug('Process was started')

    reader = GenomesReader('genomes/')
    for sequence in reader:
        logger.info(f'Исследование последовательности: {sequence.name}')
        dispatcher = SubSeqDispatcher(sequence.seq)
        result: HighestSubSeqInfo = dispatcher.highest_sub_seq()
        if result:
            logger.info(f'Наибольшая подпоследовательность длиной {result.length}'
                        f'последовательность начинается с индекса №{result.start_index}'
                        f'первый повтор начинается с индекса №{result.repeat_start_index}')

    logger.debug('Process was done')


if __name__ == '__main__':
    main()
