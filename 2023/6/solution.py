import os
import pdb
import re
from dataclasses import dataclass, field

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


def iter_races(lines: list[str]):
    time_line, distance_line = lines
    times = re.findall(r"\d+", time_line)
    distances = re.findall(r"\d+", distance_line)
    yield from ((int(time), int(distance)) for time, distance in zip(times, distances))


def parse_race(lines: list[str]):
    time_line, distance_line = lines
    times = re.findall(r"\d+", time_line)
    distances = re.findall(r"\d+", distance_line)
    return int("".join(times)), int("".join(distances))


def calculate_speeds(time: int, record_distance: int):
    for button_time in range(time):
        distance = (time - button_time) * button_time
        if distance > record_distance:
            yield button_time, distance


def do_solution(lines: list[str]):
    result = None
    for time, record_distance in iter_races(lines):
        possible = len(list(calculate_speeds(time, record_distance)))
        result = result * possible if result is not None else possible
    return result


def do_solution_2(lines: list[str]):
    time, record_distance = parse_race(lines)
    possible = len(list(calculate_speeds(time, record_distance)))

    return possible


if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)
