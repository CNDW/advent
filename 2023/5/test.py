import re

from solution import FILE, do_solution, do_solution_2, Mapper

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
    mapping = Mapper.create("test", ["50 98 2\n", "52 50 48"])
    assert mapping.map_value(0) == 0
    assert mapping.map_value(1) == 1
    assert mapping.map_value(48) == 48
    assert mapping.map_value(49) == 49
    assert mapping.map_value(50) == 52
    assert mapping.map_value(51) == 53
    assert mapping.map_value(96) == 98
    assert mapping.map_value(97) == 99
    assert mapping.map_value(98) == 50
    assert mapping.map_value(99) == 51


def test_do_solution_2():
    total = do_solution_2(EXAMPLE_LINES)

    assert total == 46
    assert False
