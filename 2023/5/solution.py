import os
import pdb
from dataclasses import dataclass, field

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


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
        return self.src_start + self.length

    @property
    def dest_end(self):
        return self.dest_start + self.length

    def __repr__(self):
        return f"{self.src_start}-{self.src_end} + ({self.offset}) = {self.dest_start}-{self.dest_end}"

    def __str__(self):
        return str(f"{self.src_start}-{self.src_end}")

    def __lt__(self, other):
        return self.src_start < other.src_start

    def map_value(self, key: str | int, debug=False):
        key = int(key)
        not_in_range = key < self.src_start or key >= self.src_end

        value = None if not_in_range else key + self.offset
        if debug:
            print(f"{self} -> {not not_in_range} {key}={value}")
        return value


@dataclass
class SeedRange:
    start: int
    end: int

    def __str__(self):
        return f"<Seeds {self.start}-{self.end}>"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, SeedRange):
            return (self.start, self.end) == (other.start, other.end)
        elif isinstance(other, tuple):
            return (self.start, self.end) == other
        raise TypeError(f"Cannot compare SeedRange to {type(other)}")

    def __lt__(self, other):
        return self.start < other.start


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

    def __repr__(self):
        return str(self)

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

    def map_range(self, seed: SeedRange) -> list[tuple[int, int]]:
        # print(f"=={self.label}==")

        if seed.end <= self.minimum or seed.start > self.maximum:
            # this seed isn't handled by the range
            # print(f"  {seed} not in mapper")
            yield seed
            return

        cursor = seed.start
        cursor_end = seed.end
        for map_range in self.ranges:
            if cursor >= map_range.src_end:
                # this seed isn't handled by this range
                # print(f"  {cursor}-{cursor_end} not in range {map_range}")
                continue
            if cursor < map_range.src_start:
                # pass through beginning part of the seed range
                # print(f"  {cursor}-{cursor_end} starts before beginning of {map_range}")
                yield SeedRange(start=cursor, end=map_range.src_start)
                cursor = map_range.src_start
                # print(f"      remainder {cursor}-{cursor_end}")
                continue

            offset = map_range.offset
            src_end = map_range.src_end
            if cursor_end > src_end:
                seed_start = cursor + offset
                seed_end = src_end + offset
                # print(f"  {cursor}-{cursor_end} ends after end of {map_range} -> new range {seed_start}-{seed_end}")

                yield SeedRange(start=seed_start, end=seed_end)
                cursor = src_end
                # print(f"      remainder {cursor}-{cursor_end}")
                continue
            else:
                # we found the end of the seed range
                # print(f"  {cursor}-{cursor_end} ends before end of {map_range}")
                yield SeedRange(start=cursor + offset, end=cursor_end + offset)
                return

        # if we get here, then we have yielded all of the ranges and have a
        # unmapped remainder
        # print(f"  {seed} ends outside of mapping")
        yield SeedRange(start=cursor, end=cursor_end)


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

    mappers.append(Mapper(label=current_label, ranges=ranges))

    return mappers


def map_value(value: int, mappers: list[Mapper]):
    for mapper in mappers:
        value = mapper.map_value(value)
    return value


def map_ranges(seed_ranges: list[SeedRange], mappers: list[Mapper]):
    for mapper in mappers:
        mapped_ranges = []
        for seed_range in seed_ranges:
            for mapped_range in mapper.map_range(seed_range):
                mapped_ranges.append(mapped_range)

        seed_ranges = mapped_ranges
    return sorted(seed_ranges)


def iter_seed_ranges(seeds: list[str]):
    index = 0

    while index < len(seeds):
        range = int(seeds[index + 1])
        start = int(seeds[index])
        end = start + range
        yield SeedRange(start=start, end=end)
        index += 2


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
    seeds = lines[0].strip().replace("seeds: ", "").split(" ")
    mappers: list[Mapper] = build_mappers(lines[1:])

    seed_ranges = list(iter_seed_ranges(seeds))
    mapped_ranges = map_ranges(seed_ranges, mappers)
    return mapped_ranges[0].start


if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)
