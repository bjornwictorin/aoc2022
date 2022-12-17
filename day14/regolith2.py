#!/usr/bin/env python3

from typing import Tuple, List

def find_cave_size(file_name: str) -> Tuple[int, int]:
    max_x = 0
    max_y = 0
    with open(file_name, "r") as f:
        for line in f:
            points = line.strip().split(" -> ")
            for point in points:
                x = int(point.split(",")[0])
                y = int(point.split(",")[1])
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    return max_x, max_y


def fill_line(cave: List[List["str"]], start: str, end: str) -> None:
    start_x, start_y = tuple(int(ii) for ii in start.split(","))
    end_x, end_y = tuple(int(ii) for ii in end.split(","))
    if start_x == end_x: # vertical line
        for yy in range(min(start_y, end_y), max(start_y, end_y) + 1):
            cave[start_x][yy] = "#"
    elif start_y == end_y: # horizontal line
        for xx in range(min(start_x, end_x), max(start_x, end_x) + 1):
            cave[xx][start_y] = "#"
    else:
        assert False, "Line must be horizontal or vertical"


def create_cave(max_x: int, max_y: int, file_name: str) -> List[List["str"]]:
    cave = [["." for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    with open(file_name, "r") as f:
        for line in f:
            points = line.strip().split(" -> ")
            for ii in range(len(points) - 1):
                fill_line(cave, points[ii], points[ii + 1])
    fill_line(cave, f"0,{max_y}", f"{max_x},{max_y}")
    return cave


def draw_cave(cave: List[List["str"]]) -> None:
    print(200 * "-")
    for yy in range(len(cave[0])):
        # TODO(bwictorin): Remove 490 limit
        for xx in range(490, len(cave)):
            print(cave[xx][yy], end = "")
        print()


def move_sand(old_pos: Tuple[int, int], cave: List[List["str"]]) -> Tuple[int, int]:
    # Drop to next rock
    old_x, old_y = old_pos
    if cave[old_x][old_y + 1] == ".":
        new_pos = (old_x, old_y + 1)
    elif cave[old_x - 1][old_y + 1] == ".":
        new_pos = (old_x - 1, old_y + 1)
    elif cave[old_x + 1][old_y + 1] == ".":
        new_pos = (old_x + 1, old_y + 1)
    else:
        new_pos = old_pos
    return new_pos


def drop_sand(cave: List[List["str"]]) -> int:
    num_sands = 0
    while True:
        # print(f"After {num_sands} units of sand")
        # draw_cave(cave)
        if cave[500][0] == "o":
            return num_sands
        old_pos = (-1, -1)
        new_pos = (500, 0)
        while old_pos != new_pos:
            old_pos = new_pos
            new_pos = move_sand(old_pos, cave)
        # if new_pos == (500, 0):
        #     return num_sands
        cave[new_pos[0]][new_pos[1]] = "o"
        num_sands += 1
    return -1


def main():
    file_name = "input.txt"
    max_x, max_y = find_cave_size(file_name)
    assert max_x >= 500
    cave = create_cave(max_x + 500, max_y + 2, file_name)
    num_sands = drop_sand(cave)
    assert num_sands != -1
    print(num_sands)


if __name__ == "__main__":
    main()
