import os
import argparse

from datetime import datetime

class Exercise00:
    STUDENT_NAME = "Joud Mawad"
    STUDENT_NAME2 = "Luis Jair Gutierrez Pacheco"

    @staticmethod
    def deadline(format_str: str) -> str:
        date = datetime(2023, 11, 15, 9, 0)
        return date.strftime(format_str)

    def __init__(self, text: str = ""):
        self.text = text

    @property
    def txt(self):
        return self.text[:17] + "..."

    @staticmethod
    def format(format_str: str):
        if format_str == "order":
            return "{2} - {1} - {0}"
        elif format_str == "dict":
            return "x, y = ({x:.1f}, {y:.4f})"
        else:
            return "wrong format"

    @staticmethod
    def listfiles(path, filetype=None):
        for root, dirs, files in os.walk(path):
            for name in files:
                if filetype is None:
                    yield name
                else:
                    ext = filetype
                if name.endswith(ext):
                    yield name

    @staticmethod
    def collatz(x: int):
        if not isinstance(x, int) or x <= 0:
            return [], 0
        collatz_list = [x]
        count = 1
        while x != 1:
            if x % 2 == 0:
                x = x // 2
                collatz_list.append(x)
                count = count + 1
            elif x != 0:
                x = 3 * x + 1
                collatz_list.append(x)
                count = count + 1
        return collatz_list, count

    def __call__(self, **kwargs):
        sorted_items = sorted(kwargs.items())
        return "\n".join(f"{k} = {v}" for k, v in sorted_items)

    def __str__(self):
        return self.encode_base64(self.text)

    @staticmethod
    def encode_base64(string: str) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        in_bytes = string.encode("utf-8") #"Joud".encode("utf-8") → [74, 111, 117, 100]
        out_chars = []

        for i in range(0, len(in_bytes), 3):
            first = in_bytes[i] #first round: 74, second round: 100
            second =in_bytes[i+1] if i+1 < len(in_bytes) else 0 #first round: 111, second round: 0
            third = in_bytes[i+2] if i+2 < len(in_bytes) else 0 #first round: 117, second round: 0

            bit_24 = (first << 16) | (second << 8) | third #first round:  01001010 01101111 01110101
                                                           #second round: 01100100 00000000 00000000

            block_1 = (bit_24 >> 18) & 0b111111 #first round: 010010, second round: 011001
            block_2 = (bit_24 >> 12) & 0b111111 #first round: 100110, second round: 000000
            block_3 = (bit_24 >> 6)  & 0b111111 #first round: 111101, second round: 000000
            block_4 =  bit_24        & 0b111111 #first round: 110101, second round: 000000

            out_chars.append(alphabet[block_1]) #first round: 18->S, second round: 25->Z
            out_chars.append(alphabet[block_2]) #first round: 38->m, second round: 0->A
            out_chars.append(alphabet[block_3]) #first round: 61->9, second round: 0->A
            out_chars.append(alphabet[block_4]) #first round: 53->1, second round: 0->A
            #first round:  out_chars = [S, m, 9, 1]
            #second round: out_chars = [S, m, 9, 1, Z, A, A, A]

        padding = len(in_bytes) % 3
        if padding == 1:
            out_chars[-2] = '='
            #out_chars = [S, m, 9, 1, Z, A, =, A]
            out_chars[-1] = '='
            #out_chars = [S, m, 9, 1, Z, A, =, =]
        elif padding == 2:
            out_chars[-1] = '='

        return "".join(out_chars) #Sm91ZA==

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("FILE", help="The input positional parameter.")
        parser.add_argument("-b", action="store_true", help="An optional boolean flag (Default: False).")
        parser.add_argument("-f", type=float, default=0.0, metavar="FLOAT", help="An optional parameter of type float (Default: 0.0).")
        parser.add_argument("-i", type=int, default=0, metavar="INT", help="An optional parameter of type int (Default: 0).")

        args = parser.parse_args()

    if __name__ == "__main__":
        main()