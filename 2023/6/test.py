import re

from solution import FILE, do_solution, do_solution_2

EXAMPLE_LINES = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 288


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 71503
