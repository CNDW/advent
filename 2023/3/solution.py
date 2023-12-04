import os
from dataclasses import dataclass
from typing import Iterable

FILE = os.path.join(os.path.dirname(__file__), "input.txt")

NON_SPECIAL_CHARS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}


@dataclass
class SchematicToken:
    x: int
    y: int
    string: str
    matrix: list[list[str]]

    def __hash__(self) -> int:
        return hash(self.string)

    @property
    def is_number(self) -> bool:
        return self.string.isdigit()

    @property
    def row(self) -> list[str]:
        return self.matrix[self.y]

    @property
    def is_null(self) -> bool:
        return self.string == "."

    def debug(self) -> str:
        top_row = "".join(item.string for item in self.iter_adjacent_edge(True)) or ""
        bottom_row = "".join(item.string for item in self.iter_adjacent_edge(False)) or ""
        left_edge = self.x if self.x == 0 else self.x - 1
        string_end = self.x + (len(self.string) - 1)
        right_edge = string_end if string_end >= len(self.row) else string_end + 1
        row = "".join(item.string for item in self.row[left_edge : right_edge + 1])
        print(f"{top_row}\n{row}\n{bottom_row}\n")

    def get_adjacent_numbers(self):
        return {char for char in self.iter_adjacent_chars() if char.is_number}

    def iter_adjacent_chars(self) -> Iterable["SchematicToken"]:
        yield from self.iter_adjacent_edge(True)
        yield from self.iter_adjacent_edge(False)
        if self.x > 0:
            yield self.row[self.x - 1]

        string_end = self.x + (len(self.string) - 1)
        if string_end < len(self.row) - 1:
            yield self.row[string_end + 1]

    def is_valid(self) -> bool:
        return any(self.is_special_char(char) for char in self.iter_adjacent_chars())

    def is_special_char(self, char: "SchematicToken") -> bool:
        return not char.is_null and not char.is_number

    def iter_adjacent_edge(self, up: bool):
        if up:
            if self.y == 0:
                return
            y_offset = -1
        else:
            if self.y == len(self.matrix) - 1:
                return
            y_offset = 1

        adjacent_row = self.matrix[self.y + y_offset]
        left_edge = self.x if self.x == 0 else self.x - 1
        string_end = self.x + (len(self.string) - 1)
        right_edge = string_end if string_end >= len(adjacent_row) - 1 else string_end + 1

        for range_x in range(left_edge, right_edge + 1):
            yield adjacent_row[range_x]


def parse(lines: Iterable[str]):
    part_numbers = []
    gear_symbols = []
    matrix: list[list[str]] = []
    for y, line in enumerate(lines):
        line = line.strip()
        matrix.append([])
        part = None
        for x, char in enumerate(line):
            if char.isdigit():
                if part is None:
                    part = SchematicToken(x, y, char, matrix)
                    part_numbers.append(part)
                else:
                    part.string += char
                matrix[y].append(part)
                continue
            if part is not None:
                part = None

            token = SchematicToken(x, y, char, matrix)
            matrix[y].append(token)
            if token.string == "*":
                gear_symbols.append(token)
    return part_numbers, gear_symbols


def do_solution(lines: Iterable[str]):
    total = 0

    part_numbers, _ = parse(lines)
    for part_number in part_numbers:
        if part_number.is_valid():
            total += int(part_number.string)
    return total


def do_solution_2(lines: Iterable[str]):
    total = 0
    _, gear_symbols = parse(lines)
    for gear_symbol in gear_symbols:
        adjacent_numbers = list(gear_symbol.get_adjacent_numbers())
        if len(adjacent_numbers) != 2:
            continue

        num1, num2 = adjacent_numbers
        total += int(num1.string) * int(num2.string)

    return total


with open(FILE, "r") as file:
    lines = list(file.readlines())

    total = do_solution(lines)
    print("TOTAL: ", total)

    total2 = do_solution_2(lines)
    print("TOTAL2: ", total2)
