import re

from solution import FILE, Hand, HandType, do_solution, do_solution_2

EXAMPLE_LINES = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip().split(
    "\n"
)


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 6440


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 5905


def test_hand_create():
    hand = Hand.create("32T3K 765")
    assert hand.bid == 765
    assert hand.type == HandType.ONE_PAIR

    hand = Hand.create("T55J5 684")
    assert hand.bid == 684
    assert hand.type == HandType.THREE_OF_A_KIND
