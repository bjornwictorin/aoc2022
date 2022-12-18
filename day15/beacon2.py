#!/usr/bin/env python3

from typing import Tuple, List, Set
import re


MAX_INDEX = 4000000


def parse_line(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    line_parts = line.strip().split(" ")
    sensor_x = int(re.split("=|,", line_parts[2])[1])
    sensor_y = int(re.split("=|:", line_parts[3])[1])
    beacon_x = int(re.split("=|,", line_parts[8])[1])
    beacon_y = int(line_parts[9].split("=")[1])
    return ((sensor_x, sensor_y), (beacon_x, beacon_y))


def get_manhattan_dist(sensor: Tuple[int, int], beacon: Tuple[int, int]) -> int:
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def find_possible_pos(no_beacon_positions: List[Set[Tuple[int, int]]]) -> Tuple[int, int]:
    pos = (-1, -1)
    for yy, row in enumerate(no_beacon_positions):
        if len(row) == 2:
            # If there is only one possible point, then only one row can contain more than one interval
            interval1 = row.pop()
            interval2 = row.pop()
            print(interval1)
            print(interval2)
            if interval1[0] < interval2[0]:
                assert interval1[1] == interval2[0] - 2
                pos = (interval2[0] - 1, yy)
            else:
                assert interval2[1] == interval1[0] - 2
                pos = (interval1[0] - 1, yy)
            break
        elif len(row) == 1:
            interval = row.pop()
            if interval[0] == 1:
                pos = (0, yy)
                break
            elif interval[1] == MAX_INDEX - 1:
                pos = (MAX_INDEX, yy)
                break
            else:
                assert interval == (0, MAX_INDEX)
        else:
            assert False, "Each line can contain only one or two intervals"

    assert pos != (-1, -1)
    return pos


def calc_freq(pos: Tuple[int, int]) -> int:
    x, y = pos
    return x * MAX_INDEX + y


def add_interval(no_beacon_positions: Set[Tuple[int, int]], lowest_x: int, highest_x: int) -> None:
    intervals_to_delete = []
    for interval in no_beacon_positions:
        interval_min, interval_max = interval
        if interval_min <= lowest_x <= interval_max and interval_min <= highest_x <= interval_max:
            assert len(intervals_to_delete) == 0
            return
        elif lowest_x <= interval_min <= highest_x and lowest_x <= interval_max <= highest_x:
            # interval is within new interval, mark for deletion
            # no_beacon_positions.discard(interval)
            intervals_to_delete.append(interval)
        elif lowest_x <= interval_min <= highest_x + 1:
            intervals_to_delete.append(interval)
            highest_x = interval_max
        elif lowest_x - 1 <= interval_max <= highest_x:
            intervals_to_delete.append(interval)
            lowest_x = interval_min
    no_beacon_positions.add((lowest_x, highest_x))
    for interval in intervals_to_delete:
        no_beacon_positions.remove(interval)


def mark_no_beacon_positions(sensor: Tuple[int, int], beacon: Tuple[int, int], no_beacon_positions: List[Set[Tuple[int, int]]]) -> None:
    sensor_x, sensor_y = sensor
    dist = get_manhattan_dist(sensor, beacon)
    lowest_y = max(0, sensor_y - dist)
    highest_y = min(MAX_INDEX, sensor_y + dist)
    for yy in range(lowest_y, highest_y + 1):
        dist_to_yy = abs(sensor_y - yy)
        lowest_x = max(0, sensor_x - (dist - dist_to_yy))
        highest_x = min(MAX_INDEX, sensor_x + (dist - dist_to_yy))
        add_interval(no_beacon_positions[yy], lowest_x, highest_x)


def main():
    no_beacon_positions = [set() for _ in range(MAX_INDEX + 1)]
    with open("input.txt", "r") as f:
        for line in f:
            sensor, beacon = parse_line(line)
            print(f"sensor: {sensor}, beacon: {beacon}")
            mark_no_beacon_positions(sensor, beacon, no_beacon_positions)
    pos = find_possible_pos(no_beacon_positions)
    freq = calc_freq(pos)
    print(freq)


if __name__ == "__main__":
    main()
