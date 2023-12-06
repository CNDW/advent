import os
import pdb
from dataclasses import dataclass, field

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class RangeMap:
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

    def split(self, at: int):
        if at <= self.start or at >= self.end:
            raise ValueError(f"Cannot split {self} at {at}")
        return SeedRange(start=self.start, end=at), SeedRange(start=at, end=self.end)

    def apply_offset(self, offset: int):
        self.start += offset
        self.end += offset

    def is_in_range(self, range_map: RangeMap):
        return self.start >= range_map.src_start and self.end <= range_map.src_end


@dataclass
class Mapper:
    label: str
    ranges: list[RangeMap]
    minimum: int = 0
    maximum: int = 0
    split_points: list[int] = field(default_factory=list)

    def __str__(self):
        return f"{self.label} ({self.minimum}-{self.maximum})\n  " + "\n  ".join(
            list(str(map_range) for map_range in self.ranges)
        )

    def __repr__(self):
        return str(self)

    def __post_init__(self):
        self.ranges = sorted(self.ranges)
        split_points = set()
        for range in self.ranges:
            split_points.add(range.src_start)
            split_points.add(range.src_end)
        self.split_points = sorted(split_points)

    @classmethod
    def create(cls, label: str, lines: list[str]):
        return cls(label=label, ranges=[RangeMap.create(line) for line in lines])

    def map_value(self, key: str | int, debug=False):
        key = int(key)
        for map_range in self.ranges:
            value = map_range.map_value(key, debug=debug)
            if value is not None:
                return value

        return key

    def apply_offset(self, seed: SeedRange):
        for range_map in self.ranges:
            if not seed.is_in_range(range_map):
                continue

            seed.apply_offset(range_map.offset)
            break

    def iter_splits(self, seed: SeedRange):
        for split_point in self.split_points:
            if split_point >= seed.end or split_point <= seed.start:
                continue

            before, after = seed.split(split_point)
            yield from self.iter_splits(before)
            yield from self.iter_splits(after)
            return
        yield seed

    def map_range(self, seed: SeedRange):
        for _seed in self.iter_splits(seed):
            self.apply_offset(_seed)
            yield _seed


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
            ranges.append(RangeMap.create(line))

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
