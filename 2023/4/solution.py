import os
import re
from dataclasses import dataclass
from typing import Iterable

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def parse_card(line: str):
    card_match = re.findall(r"^(Card \d+):", line)
    assert card_match, f"Card not found in {line}"
    return card_match[0]


def parse_numbers(line: str):
    winners, numbers = line.split(":")[1].split("|")

    winners_match = re.findall(r"\d+", winners)
    numbers_match = re.findall(r"\d+", numbers)
    return set(winners_match), numbers_match


def score_line(line: str):
    winners, numbers = parse_numbers(line)
    score = 0
    for number in numbers:
        if number not in winners:
            continue
        score = score * 2 if score != 0 else 1
    return score


def get_match_count(line: str):
    winners, numbers = parse_numbers(line)
    count = 0
    for number in numbers:
        if number in winners:
            count += 1
    return count


def do_solution(lines: Iterable[str]):
    total = 0
    for line in lines:
        score = score_line(line)
        total += score

    return total


def do_solution_2(lines: Iterable[str]):
    total = 0
    dupes = []
    for line in lines:
        if dupes:
            dupe_count = dupes.pop(0)
            card_count = dupe_count + 1
        else:
            dupe_count = 0
            card_count = 1
        total += card_count

        match_count = get_match_count(line)
        for idx in range(match_count):
            if idx >= len(dupes):
                dupes.append(1 * card_count)
            else:
                dupes[idx] += 1 * card_count

    return total


with open(FILE, "r") as file:
    lines = list(file.readlines())

    total = do_solution(lines)
    print("TOTAL: ", total)

    total2 = do_solution_2(lines)
    print("TOTAL2: ", total2)
