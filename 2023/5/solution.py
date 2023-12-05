import os
import re
from dataclasses import dataclass, field
from typing import NamedTuple

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


class RangeConversion(NamedTuple):
    src_start: int
    src_end: int
    dest_start: int
    dest_end: int

@dataclass
class MapRange:
    src_start: int
    dest_start: int
    length: int
    offset: int

    @classmethod
    def create(cls, line: str):
        dest_start, src_start, length = line.strip().split(" ")
        return cls(
            src_start=int(src_start),
            dest_start=int(dest_start),
            length=int(length),
            offset=int(dest_start) - int(src_start),
        )

    @property
    def src_end(self):
        return self.src_start + self.length - 1

    def __str__(self):
        return f"{self.src_start}-{self.src_end} - ({self.offset}) = {self.dest_start}-{self.dest_end}"

    def __lt__(self, other):
        return self.src_start < other.src_start

    @property
    def dest_end(self):
        return self.dest_start + self.length - 1

    def map_value(self, key: str | int, debug=False):
        key = int(key)
        not_in_range = key < self.src_start or key > self.src_end

        value = None if not_in_range else key + self.offset
        if debug:
            print(f"{self} -> {not not_in_range} {key}={value}")
        return value


@dataclass
class Mapper:
    label: str
    ranges: list[MapRange]
    minimum: int = 0
    maximum: int = 0

    def __str__(self):
        return f"{self.label} ({self.minimum}-{self.maximum})\n  " + "\n  ".join(
            list(str(map_range) for map_range in self.ranges)
        )

    def __post_init__(self):
        self.ranges = sorted(self.ranges)
        self.minimum = self.ranges[0].src_start
        self.maximum = self.ranges[-1].src_end

    @classmethod
    def create(cls, label: str, lines: list[str]):
        return cls(label=label, ranges=[MapRange.create(line) for line in lines])

    def map_value(self, key: str | int, debug=False):
        key = int(key)
        if key < self.minimum or key > self.maximum:
            return key
        for map_range in self.ranges:
            value = map_range.map_value(key, debug=debug)
            if value is not None:
                return value

        return key
    
    def map_range(start: int, end: int) -> list[]


def build_mappers(lines: list[str]) -> list[Mapper]:
    mappers: list[Mapper] = []
    ranges = []
    current_label = None
    for line in lines:
        line = line.strip()
        if line == "":
            continue

        if line.endswith(" map:"):
            if current_label:
                mappers.append(Mapper(label=current_label, ranges=ranges))
            current_label = line.replace(" map:", "")
            ranges = []
        else:
            ranges.append(MapRange.create(line))

    for mapper in mappers:
        print(mapper)
    return mappers


def map_value(value: int, mappers: list[Mapper]):
    for mapper in mappers:
        value = mapper.map_value(value)
    return value


def iter_seed_ranges(seeds: list[str]):
    total = len(seeds) // 2

    for idx in range(total):
        pair_index = idx * 2
        seed_range = int(seeds[pair_index + 1])
        seed_start = int(seeds[(pair_index)])

        yield seed_start, seed_range


def iter_range(start: int, length: int):
    for idx in range(length):
        seed = start + idx
        yield seed


def do_solution(lines: list[str]):
    result = None
    seeds = lines[0].strip().replace("seeds: ", "").split(" ")
    mappers: list[Mapper] = build_mappers(lines[1:])

    for seed in seeds:
        value: int = map_value(int(seed), mappers)
        if result is None or value < result:
            result = value
    return result


def do_solution_2(lines: list[str]):
    result = None
    seeds = lines[0].strip().replace("seeds: ", "").split(" ")
    mappers: list[Mapper] = build_mappers(lines[1:])
    value = None
    lowest_seed = None
    for seed_start, seed_range in iter_seed_ranges(seeds):
        for seed in iter_range(seed_start, seed_range):
            value = map_value(seed, mappers)

            if result is None or value < result:
                lowest_seed = seed
                result = value
    print(f"LOWEST: {lowest_seed} MAPPED: {result}")
    return result


if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)
