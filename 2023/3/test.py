import re

from solution import FILE, do_solution, do_solution_2, parse

EXAMPLE_LINES = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 4361


def test_number_is_valid():
    part_numbers, _ = parse(EXAMPLE_LINES)

    invalid_numbers = {1, 5}
    for index, part_number in enumerate(part_numbers):
        is_valid = index not in invalid_numbers
        assert (
            part_number.is_valid() == is_valid
        ), f"part {part_number.string} is should be {is_valid} but returned {not is_valid}"


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 467835


def test_solution_count():
    with open(FILE, "r") as file:
        input = file.read()

    part_numbers, _ = parse(input.splitlines())

    assert len(part_numbers) == 1211

    groups = re.findall(r"\d+", input)
    assert set(groups) == set(part.string for part in part_numbers)
    assert len(groups) == 1211
