import re

from solution import FILE, do_solution, do_solution_2

EXAMPLE_LINES = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".strip().split(
    "\n"
)

EXAMPLE_LINES_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip().split(
    "\n"
)

EXAMPLE_LINES_3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".strip().split(
    "\n"
)


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 2

    total = do_solution(EXAMPLE_LINES_2)

    assert total == 6


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES_3)

    assert total == 6
