class DictGenerator:
    def __init__(self, alphabet: list):
        self.alphabet = alphabet

    def generate(self, length: int) -> list:
        result = []
        alphabet_len = len(self.alphabet)
        max_val = int(''.join([str(alphabet_len - 1) for i in range(length)]))
        combinations = range(0, max_val + 1)
        combinations = map(lambda x: self.convert_to_str(x, length), combinations)
        combinations = filter(lambda x: self.less_alphabet_len(x), combinations)
        for digit in combinations:
            digit_str = self.convert_to_str(digit, length)
            for index, smb in enumerate(digit_str):
                digit_str = self.replace_smb(digit_str, index, self.alphabet[int(smb)])
            result.append(digit_str)

        return result

    def convert_to_str(self, digit: int, str_len: int):
        str_digit = str(digit)
        return self.generate_zero_str(str_len - len(str_digit)) + str_digit

    def less_alphabet_len(self, digit_str: str) -> bool:
        result = True
        for smb in digit_str:
            if int(smb) > len(self.alphabet) - 1:
                result = False
                break
        return result

    @staticmethod
    def generate_zero_str(length: int):
        first_smb = '0'
        result = [first_smb for _ in range(0, length)]
        return ''.join(result)

    @staticmethod
    def replace_smb(string: str, index: int, smb: str) -> str:
        return ''.join([string[:index], smb, string[index + 1:]])


if __name__ == '__main__':
    dg = DictGenerator(['A', 'C', 'G', 'T'])
    print(dg.generate(1))
    print(dg.generate(2))
    print(dg.generate(3))
