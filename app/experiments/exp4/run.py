import csv
import math
import pandas

from openpyxl import Workbook
from openpyxl.styles.fills import GradientFill, Stop, Color

from typing import List
from logger import logger
from utils import GenomesReader
from utils.seq_pair import SeqPair
from Bio.SeqRecord import SeqRecord
from utils.results_rw import ResultsRW
from typing import Optional, NamedTuple
from utils.dict_generator import DictGenerator
from concurrent.futures import ProcessPoolExecutor, wait
from modules.pattern_searcher import (
    SearchResult,
    BrutePairSearcher
)


class GenomeColor(NamedTuple):
    genome_id: str
    color: str


class Application:
    ALPHABET = ['A', 'C', 'G', 'T']
    GENOMES_PATH = '../../genomes/'

    def __init__(self):
        reader = GenomesReader(self.GENOMES_PATH)
        self.genomes: List[SeqRecord] = list(reader)
        self.genome_colors = self.read_colors('diseases_types.csv')

    def run(self):
        wb = Workbook()
        ws = wb.active

        self.add_headers(ws)

        table = [
            ['', *[gen.id for gen in self.genomes]]
        ]
        for index, first_gen in enumerate(self.genomes):
            row = [first_gen.id]
            for second_gen in self.genomes:
                first_color = Color(self.get_color(first_gen.id), type='rgba')
                second_color = Color(self.get_color(second_gen.id), type='rgba')
                row.append(GradientFill(
                    type='linear',
                    degree=45,
                    stop=(
                        Stop(first_color, 0),
                        Stop(second_color, 1)
                    )
                ))
            table.append(row)

        for row_index, row in enumerate(table):
            for col_index, value in enumerate(row):
                cell = ws.cell(row_index + 1, col_index + 1)
                if isinstance(value, GradientFill):
                    cell.fill = value
                else:
                    cell.value = value

        wb.save('results/result.xlsx')

    def add_headers(self, ws):
        for index, genome in enumerate(self.genomes):
            ws.cell(1, index + 2)
            ws.cell(index + 2, 1).value = genome.id

    def get_color(self, genome_id: str) -> str:
        result = None
        for gen_color in self.genome_colors:
            if gen_color.genome_id == genome_id:
                result = gen_color.color
        return result

    @staticmethod
    def read_colors(file_name: str) -> List[GenomeColor]:
        result = []
        with open(file_name) as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                result.append(GenomeColor(
                    genome_id=row[0],
                    color=row[1]
                ))
        return result


if __name__ == '__main__':
    Application().run()