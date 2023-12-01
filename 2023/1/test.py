from solution import read_lines, read_number_from_line


def test_read_lines():
    lines = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]

    total = read_lines(lines)

    assert total == 281


def test_read_number_from_line():
    assert read_number_from_line("two1nine") == 29
    assert read_number_from_line("veightwochrmfrkrcppxkj4tvvzmhqjhnjvtq1threegtmfnnjpxb") == 83
    assert read_number_from_line("rvnone3three9twozchp26") == 16
    assert read_number_from_line("eightthree3ninekzhtlqsevenssprmrqhhgncrs") == 87
    assert read_number_from_line("ninezjtxp7bpzdgtoneeightoneighth") == 98
