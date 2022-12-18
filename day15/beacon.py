#!/usr/bin/env python3

from typing import Tuple, Set
import re

def parse_line(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    line_parts = line.strip().split(" ")
    sensor_x = int(re.split("=|,", line_parts[2])[1])
    sensor_y = int(re.split("=|:", line_parts[3])[1])
    beacon_x = int(re.split("=|,", line_parts[8])[1])
    beacon_y = int(line_parts[9].split("=")[1])
    return ((sensor_x, sensor_y), (beacon_x, beacon_y))


def get_manhattan_dist(sensor: Tuple[int, int], beacon: Tuple[int, int]) -> int:
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def mark_no_beacon_positions(sensor: Tuple[int, int], beacon: Tuple[int, int], special_line_y: int, no_beacon_positions: Set[int]) -> None:
    sensor_x, sensor_y = sensor
    beacon_x, beacon_y = beacon
    dist = get_manhattan_dist(sensor, beacon)
    dist_to_spc_line = abs(sensor_y - special_line_y)
    lowest_x = sensor_x - (dist - dist_to_spc_line)
    highest_x = sensor_x + (dist - dist_to_spc_line)
    for xx in range(lowest_x, highest_x + 1):
        no_beacon_positions.add(xx)
    if beacon_y == special_line_y:
        no_beacon_positions.discard(beacon_x)

def main():
    special_line_y = 2000000 # 10 # Remember to change to 2000000 for real input data
    no_beacon_positions = set() # Use set to avoid duplicates
    with open("input.txt", "r") as f:
        for line in f:
            sensor, beacon = parse_line(line)
            print(f"sensor: {sensor}, beacon: {beacon}")
            mark_no_beacon_positions(sensor, beacon, special_line_y, no_beacon_positions)
    print(len(no_beacon_positions))


if __name__ == "__main__":
    main()
