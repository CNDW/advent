import os
from typing import Iterable
from itertools import chain

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def get_game_id(line: str) -> int:
    game_id, _ = line.split(":")
    return int(game_id.strip().split(" ")[1])


def iter_dice(line: str) -> tuple[str, int]:
    _, tries = line.split(":")
    tries = tries.strip().split("; ")
    for seen_dice in tries:
        colors = seen_dice.split(", ")
        assert len(colors) <= 3
        assert len(set(items.split(" ")[1] for items in colors)) <= 3
        for count, color in chain(items.split(" ") for items in colors):
            yield color, int(count)


MAX_COUNTS = {"red": 12, "green": 13, "blue": 14}


def is_valid(line: str) -> bool:
    for color, count in iter_dice(line):
        if count > MAX_COUNTS[color]:
            return False
    return True


def find_minimum_power(line: str) -> dict[str, int]:
    minimums = {}
    for color, count in iter_dice(line):
        if minimums.get(color, 0) < count:
            minimums[color] = count
    return minimums["red"] * minimums["blue"] * minimums["green"]


def do_solution(lines: Iterable[str]):
    total = 0

    for line in lines:
        game_id = get_game_id(line)
        if is_valid(line):
            total += game_id

    return total


def do_solution_2(lines: Iterable[str]):
    total = 0

    for line in lines:
        game_id = get_game_id(line)
        power = find_minimum_power(line)
        total += power

    return total


with open(FILE, "r") as file:
    lines = list(file.readlines())

    total = do_solution(lines)
    print("TOTAL: ", total)

    total2 = do_solution_2(lines)
    print("TOTAL2: ", total2)
