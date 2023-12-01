import os
from typing import Iterable

FILE = os.path.join(os.path.dirname(__file__), "input.txt")

WORD_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
WORD_TREE = {}
for word, number in WORD_MAP.items():
    current = WORD_TREE
    for index, char in enumerate(word):
        if index < len(word) - 1:
            current = current.setdefault(char, {})
        else:
            current[char] = number


def scan_for_number(line: str) -> int | None:
    current = WORD_TREE
    for char in line:
        if char not in current:
            break
        current = current.get(char)
        if type(current) is int:
            return current


def read_number_from_line(line: str) -> int:
    line = line.strip().lower()
    first_number = None
    last_number = None

    for index, char in enumerate(line):
        if char.isdigit():
            number = int(char)
        else:
            number = scan_for_number(line[index:])
            if number is None:
                continue

        if first_number is None:
            first_number = number
        last_number = number

    combined = int(f"{first_number}{last_number}")
    return combined


def read_lines(lines: Iterable[str]):
    total = 0
    for line in lines:
        if line == "":
            continue

        combined = read_number_from_line(line)
        total += combined
        print(combined, total)

    return total


with open(FILE, "r") as file:
    total = read_lines(file.readlines())

    print("TOTAL: ", total)
