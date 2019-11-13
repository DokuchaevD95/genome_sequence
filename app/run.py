from logger import logger
from utils import GenomesReader


def main():
    logger.debug('Process was started')
    reader = GenomesReader('genomes')
    for seq in reader:
        print(seq)
    logger.debug('Process was done')


if __name__ == '__main__':
    main()
