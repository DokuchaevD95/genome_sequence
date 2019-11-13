from logger import logger
from utils import GenomesReader
from sub_seq_dispatcher import SubSeqDispatcher, HighestSubSeqInfo


def main():
    logger.debug('Process was started')

    reader = GenomesReader('genomes/')
    for sequence in reader:
        dispatcher = SubSeqDispatcher(sequence.seq)
        result: HighestSubSeqInfo = dispatcher.highest_sub_seq()

    logger.debug('Process was done')


if __name__ == '__main__':
    main()
