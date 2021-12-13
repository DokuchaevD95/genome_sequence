import pandas as pd
from Bio import SeqRecord
from typing import List, NamedTuple, Optional
from utils.genomes_reader import GenomesReader
from utils.sequence_dispatcher import SequenceDispatcher
from concurrent.futures import ProcessPoolExecutor, as_completed
from modules.pattern_searcher import PairSubSeqSearcher, SearchResult


class Application:
    ALPHABET = ['A', 'C', 'G', 'T']
    GENOMES_PATH = '../../genomes/'

    def __init__(self):
        reader = GenomesReader(self.GENOMES_PATH)
        self.genomes: List[SeqRecord] = list(reader)
        self.genomes = self.genomes[:4]

    def get_len_frame(self):
        pass

    def find_in_pair(self, first: SeqRecord, second: SeqRecord) -> Optional[SearchResult]:
        if first.id == second.id:
            return None
        return PairSubSeqSearcher(first, second).tzarev(15)

    def find_repeats(self) -> List[SearchResult]:
        result = []
        with ProcessPoolExecutor() as executor:
            futures = []
            for i in range(len(self.genomes)):
                for j in range(i + 1, len(self.genomes)):
                    future = executor.submit(
                        self.find_in_pair,
                        self.genomes[i],
                        self.genomes[j]
                    )
                    futures.append(future)

            for future in as_completed(futures):
                result.append(future.result())

        return result

    def collect_stats(self) -> List[pd.DataFrame]:
        pass

    def run(self):
        repeats = self.find_repeats()


if __name__ == '__main__':
    Application().run()
