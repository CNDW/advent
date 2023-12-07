import re
from itertools import chain

import pytest
from solution import Mapper, SeedRange, build_mappers, do_solution, do_solution_2, iter_seed_ranges, map_ranges

# seed range [seed_start, length]
# mapping = [dest_start, source_start, length]
EXAMPLE_LINES = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


def test_do_solution():
    total = do_solution(EXAMPLE_LINES)

    assert total == 35


def test_create_mapping():
    mapper = Mapper.create("test", ["50 98 2\n", "52 50 48"])
    assert mapper.map_value(0) == 0
    assert mapper.map_value(1) == 1
    assert mapper.map_value(48) == 48
    assert mapper.map_value(49) == 49
    assert mapper.map_value(50) == 52
    assert mapper.map_value(51) == 53
    assert mapper.map_value(96) == 98
    assert mapper.map_value(97) == 99
    assert mapper.map_value(98) == 50
    assert mapper.map_value(99) == 51


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 46


def test_map_ranges():
    seed_ranges = list(iter_seed_ranges(["79", "14", "55", "13"]))
    mapper = Mapper.create(
        "seed-to-soil",
        [
            "50 98 2",
            "52 50 48",
        ],
    )

    result = list(chain.from_iterable(mapper.map_range(seed_range) for seed_range in seed_ranges))

    assert result == [(81, 95), (57, 70)]


def test_map_ranges_2():
    seed_range = SeedRange(start=57, end=69)
    mapper = Mapper.create(
        "fertilizer-to-water",
        [
            "49 53 8",
            "0 11 42",
            "42 0 7",
            "57 7 4",
        ],
    )
    """
    57-69
    fertilizer-to-water (0-60)
        0-6 + (42) = 42-48
        7-10 + (50) = 57-60
        11-52 + (-11) = 0-41
        53-60 + (-4) = 49-56 ~ 57-60 -> 53-56
    (unhandled: 61-69)
    53-56, 61-69
    """
    result = list(mapper.map_range(seed_range))
    assert result == [(53, 57), (61, 69)]


def test_map_ranges_3():
    mapper = Mapper.create(
        "light-to-temperature",
        [
            "45 77 23",
            "81 45 19",
            "68 64 13",
        ],
    )
    seed_range = next(iter_seed_ranges(["74", "14"]))  # 74-87

    result = list(mapper.map_range(seed_range))
    assert sorted(result) == [(45, 56), (78, 81)]


def test_map_ranges_4():
    mappers = build_mappers(EXAMPLE_LINES[1:])
    seed_ranges = list(iter_seed_ranges(["74", "14", "55", "13"]))

    result = list(map_ranges(seed_ranges, mappers))
    assert sorted(result) == [(46, 52), (56, 60), (77, 85), (86, 90), (94, 97), (97, 99)]


def test_seed_split():
    seed_range = next(iter_seed_ranges(["74", "14"]))  # 74-87

    assert seed_range.split(75) == ((74, 75), (75, 88))
    assert seed_range.split(80) == ((74, 80), (80, 88))
    with pytest.raises(ValueError):
        seed_range.split(74)
    with pytest.raises(ValueError):
        seed_range.split(88)
    with pytest.raises(ValueError):
        seed_range.split(90)
    with pytest.raises(ValueError):
        seed_range.split(20)
