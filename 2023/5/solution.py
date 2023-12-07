import os
import pdb
from dataclasses import dataclass, field

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class MapperRange:
    start: int
    end: int
    offset: int

    @classmethod
    def create(cls, line: str):
        dest_start, start, length = line.strip().split(" ")
        start = int(start)
        return cls(
            start=start,
            end=start + int(length),
            offset=int(dest_start) - start,
        )

    def __repr__(self):
        return f"<Mapper {self.start}-{self.end} ({self.offset})>"

    def __str__(self):
        return str(f"{self.start}-{self.end}")

    def __lt__(self, other):
        return self.start < other.start

    def map_value(self, key: str | int):
        key = int(key)

        not_in_range = key < self.start or key >= self.end
        return None if not_in_range else key + self.offset


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

    def __lt__(self, other: "SeedRange"):
        return self.start < other.start

    def split(self, at: int):
        if at <= self.start or at >= self.end:
            raise ValueError(f"Cannot split {self} at {at}")
        return SeedRange(start=self.start, end=at), SeedRange(start=at, end=self.end)

    def apply_offset(self, offset: int):
        self.start += offset
        self.end += offset

    def is_in_range(self, mapper_range: MapperRange):
        return self.start >= mapper_range.start and self.end <= mapper_range.end


@dataclass
class Mapper:
    label: str
    ranges: list[MapperRange]
    split_points: list[int] = field(default_factory=list)

    def __str__(self):
        return f"<Mapper {self.label}>\n  " + "\n  ".join(list(str(map_range) for map_range in self.ranges))

    def __repr__(self):
        return str(self)

    def __post_init__(self):
        self.ranges = sorted(self.ranges)
        split_points = set()
        for range in self.ranges:
            split_points.add(range.start)
            split_points.add(range.end)
        self.split_points = sorted(split_points)

    @classmethod
    def create(cls, label: str, lines: list[str]):
        return cls(label=label, ranges=[MapperRange.create(line) for line in lines])

    def map_value(self, key: str | int):
        key = int(key)
        for map_range in self.ranges:
            value = map_range.map_value(key)
            if value is not None:
                return value

        return key

    def apply_offset(self, seed: SeedRange):
        for mapper_range in self.ranges:
            if not seed.is_in_range(mapper_range):
                continue

            seed.start += mapper_range.offset
            seed.end += mapper_range.offset
            break

    def iter_splits(self, seed: SeedRange):
        for split_point in self.split_points:
            if split_point >= seed.end or split_point <= seed.start:
                # Split point is not in range, ignore
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
            ranges.append(MapperRange.create(line))

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
        length = int(seeds[index + 1])
        start = int(seeds[index])
        end = start + length
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
    seed_lines = lines[0].strip().replace("seeds: ", "").split(" ")
    mappers: list[Mapper] = build_mappers(lines[1:])

    seed_ranges = list(iter_seed_ranges(seed_lines))
    mapped_ranges = map_ranges(seed_ranges, mappers)
    return mapped_ranges[0].start


if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)
