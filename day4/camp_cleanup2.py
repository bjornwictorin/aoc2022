#!/usr/bin/env python3

import re
from typing import Tuple


def is_subrange(interval_a: Tuple[int, int], interval_b: Tuple[int, int]) -> bool:
    if interval_a[0] >= interval_b[0] and interval_a[1] <= interval_b[1]:
        return True
    return False


def do_overlap(interval_a: Tuple[int, int], interval_b: Tuple[int, int]) -> bool:
    if interval_a[1] >= interval_b[1]:
        highest_interval = interval_a
        lowest_interval = interval_b
    else:
        highest_interval = interval_b
        lowest_interval = interval_a
    return highest_interval[0] <= lowest_interval[1]


def main():
    num_overlapping_pairs = 0
    with open("input.txt", "r") as f:
        for line in f:
            range_ends = tuple(int(ii) for ii in re.split("-|,", line))
            assert len(range_ends) == 4
            first_range = range_ends[:2]
            second_range = range_ends[2:]
            assert len(first_range) == 2
            assert len(second_range) == 2
            if do_overlap(first_range, second_range):
                num_overlapping_pairs += 1
    print(num_overlapping_pairs)


if __name__ == "__main__":
    main()
