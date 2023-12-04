import re

from solution import FILE, do_solution, do_solution_2, score_line

EXAMPLE_LINES = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 17 82 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 13


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 30


def test_score_line():
    assert score_line(EXAMPLE_LINES[0]) == 8
    assert score_line(EXAMPLE_LINES[1]) == 2
    assert score_line(EXAMPLE_LINES[2]) == 2
    assert score_line(EXAMPLE_LINES[3]) == 1
    assert score_line(EXAMPLE_LINES[4]) == 0
    assert score_line(EXAMPLE_LINES[5]) == 0
