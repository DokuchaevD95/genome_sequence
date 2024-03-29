import math
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

    def get_len_frame(self, repeats: List[SearchResult]) -> pd.DataFrame:
        index = columns = [genome.id for genome in self.genomes]
        frame = pd.DataFrame(index=index, columns=columns)

        for repeat in repeats:
            if repeat:
                first_id = repeat.first_rec.id
                sec_id = repeat.second_rec.id
                frame.at[first_id, sec_id] = frame.at[sec_id, first_id] = repeat.length

        return frame

    def get_ln_statement_to_avr_len(self, repeats: List[SearchResult]) -> pd.DataFrame:
        index = columns = [genome.id for genome in self.genomes]
        frame = pd.DataFrame(index=index, columns=columns)

        for repeat in repeats:
            if repeat:
                first_id = repeat.first_rec.id
                sec_id = repeat.second_rec.id
                avr = (len(repeat.first_rec.seq) + len(repeat.second_rec.seq)) / 2
                value = repeat.length / math.log(avr)
                frame.at[first_id, sec_id] = frame.at[sec_id, first_id] = value

        return frame

    def get_sqr_statement_to_len(self, repeats: List[SearchResult]) -> pd.DataFrame:
        index = columns = [genome.id for genome in self.genomes]
        frame = pd.DataFrame(index=index, columns=columns)

        for repeat in repeats:
            if repeat:
                first_id = repeat.first_rec.id
                sec_id = repeat.second_rec.id
                sq_sum = (len(repeat.first_rec.seq) ** 2) + (len(repeat.second_rec.seq) ** 2)
                value = repeat.length / math.sqrt(sq_sum)
                frame.at[first_id, sec_id] = frame.at[sec_id, first_id] = value

        return frame

    def get_avr_ln_to_len(self, repeats: List[SearchResult]) -> pd.DataFrame:
        index = columns = [genome.id for genome in self.genomes]
        frame = pd.DataFrame(index=index, columns=columns)

        for repeat in repeats:
            if repeat:
                first_id = repeat.first_rec.id
                sec_id = repeat.second_rec.id
                avr = (math.log(len(repeat.first_rec.seq)) + math.log(len(repeat.second_rec.seq))) / 2
                value = repeat.length / avr
                frame.at[first_id, sec_id] = frame.at[sec_id, first_id] = value

        return frame

    def get_ln_to_sqr(self, repeats: List[SearchResult]) -> pd.DataFrame:
        index = columns = [genome.id for genome in self.genomes]
        frame = pd.DataFrame(index=index, columns=columns)

        for repeat in repeats:
            if repeat:
                first_id = repeat.first_rec.id
                sec_id = repeat.second_rec.id
                mul = len(repeat.first_rec.seq) * len(repeat.second_rec.seq)
                value = repeat.length / math.log(math.sqrt(mul))
                frame.at[first_id, sec_id] = frame.at[sec_id, first_id] = value

        return frame

    def collect_stats(self, repeats: List[SearchResult]):
        len_dataframe = self.get_len_frame(repeats)
        ln_to_avr_len_dataframe = self.get_ln_statement_to_avr_len(repeats)
        arv_ln_to_len = self.get_avr_ln_to_len(repeats)
        sqr_dataframe = self.get_sqr_statement_to_len(repeats)
        ln_to_sqr = self.get_ln_to_sqr(repeats)

        writer = pd.ExcelWriter('output.xlsx')

        len_dataframe.to_excel(writer, sheet_name='LEN')
        ln_to_avr_len_dataframe.to_excel(writer, sheet_name='LEN div ln((N1 add N2) div 2)')
        arv_ln_to_len.to_excel(writer, sheet_name='LEN div ((ln(N1) add ln(N2)) div 2)')
        sqr_dataframe.to_excel(writer, sheet_name='LEN div sqrt(N1^2 add N2^2)')
        ln_to_sqr.to_excel(writer, sheet_name='LEN div ln(sqrt(N1 mul N2))')


        writer.save()

    def run(self):
        repeats = self.find_repeats()

        self.collect_stats(repeats)


if __name__ == '__main__':
    Application().run()
