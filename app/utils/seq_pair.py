from typing import NamedTuple


class SeqPair(NamedTuple):
    first_seq: str
    sec_seq: str

    def check(self, first_name, second_name) -> bool:
        return (
            self.first_seq == first_name or self.sec_seq == first_name
        ) and (
            self.first_seq == second_name or self.sec_seq == second_name
        )

    def __repr__(self):
        return f'{self.first_seq} / {self.sec_seq}'

    def __eq__(self, other: 'SeqPair') -> bool:
        return (
            self.first_seq == other.first_seq or self.sec_seq == other.first_seq
        ) and (
            self.first_seq == other.sec_seq or self.sec_seq == other.sec_seq
        )
