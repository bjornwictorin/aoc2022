#!/usr/bin/env python3

from enum import Enum
from typing import Tuple, List, Set

class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def dot_index(line: str) -> int:
    return line.find(".")


def parse_input(file_name: str) -> Tuple[List[Set[Tuple[int, int]]], Tuple[int, int], Tuple[int, int], int, int]:
    blizzards = [set(), set(), set(), set()]
    start = (0, 0)
    goal = (0, 0)
    width = 0
    height = 0
    with open(file_name, "r") as f:
        for yy, line in enumerate(f):
            line = line.strip()
            if 0 == yy:
                start = (dot_index(line), 0)
            elif len(set(line)) == 2: # Only "#" and "." in last line
                goal = (dot_index(line), yy)
                width = len(line) - 2
                height = yy - 1
            else:
                for xx, val in enumerate(line):
                    if val == "^":
                        blizzards[Directions.NORTH.value].add((xx, yy))
                    elif val == ">":
                        blizzards[Directions.EAST.value].add((xx, yy))
                    elif val == "v":
                        blizzards[Directions.SOUTH.value].add((xx, yy))
                    elif val == "<":
                        blizzards[Directions.WEST.value].add((xx, yy))
                    else:
                        assert(val == "." or val == "#")
    return blizzards, start, goal, height, width


def update_blizzards(blizzards: List[Set[Tuple[int, int]]], height: int, width: int) -> None:
    moved_blizzards = [set(), set(), set(), set()]
    for direction, blizzard_set in enumerate(blizzards):
        for blizzard in blizzard_set:
            old_x, old_y = blizzard
            if direction == Directions.NORTH.value:
                moved_blizzards[direction].add((old_x, ((old_y - 1 + height - 1) % height) + 1))
            elif direction == Directions.EAST.value:
                moved_blizzards[direction].add((((old_x + 1 - 1) % width + 1), old_y))
            elif direction == Directions.SOUTH.value:
                moved_blizzards[direction].add((old_x, ((old_y + 1 - 1) % height + 1)))
            elif direction == Directions.WEST.value:
                moved_blizzards[direction].add(((old_x - 1 + width - 1) % width + 1, old_y))
    for ii in range(4):
        blizzards[ii] = moved_blizzards[ii]


def windy(pos: Tuple[int, int], blizzards: List[Set[Tuple[int, int]]]) -> bool:
    is_windy = False
    for direction in blizzards:
        if pos in direction:
            is_windy = True
    return is_windy


def find_new_possible_pos(possible_positions: Set[Tuple[int, int]], blizzards: List[Set[Tuple[int, int]]], height: int, width: int) -> Set[Tuple[int, int]]:
    moved_positions = set()
    for pos in possible_positions:
        old_x, old_y = pos
        if not windy(pos, blizzards):
            moved_positions.add(pos) # Stay in same pos
        if old_y > 1 and not windy((old_x, old_y - 1), blizzards):
            moved_positions.add((old_x, old_y - 1)) # north
        if old_x < width and 0 < old_y < height + 1 and not windy((old_x + 1, old_y), blizzards):
            moved_positions.add((old_x + 1, old_y)) # east
        if old_y < height and not windy((old_x, old_y + 1), blizzards):
            moved_positions.add((old_x, old_y + 1)) # south
        if old_x > 1 and 0 < old_y < height + 1 and not windy((old_x - 1, old_y), blizzards):
            moved_positions.add((old_x - 1, old_y)) # west
    return moved_positions


def main():
    blizzards, start, goal, height, width = parse_input("input.txt")
    goal_x, goal_y = goal
    start_x, start_y = start
    # Start to goal
    possible_positions = {start}
    round = 0
    while True:
        update_blizzards(blizzards, height, width)
        possible_positions = find_new_possible_pos(possible_positions, blizzards, height, width)
        round += 1
        if (goal_x, goal_y - 1) in possible_positions:
            break
    round += 1
    update_blizzards(blizzards, height, width)
    print(round)

    # Goal to start
    possible_positions = {goal}
    while True:
        update_blizzards(blizzards, height, width)
        possible_positions = find_new_possible_pos(possible_positions, blizzards, height, width)
        round += 1
        if (start_x, start_y + 1) in possible_positions:
            break
    round += 1
    update_blizzards(blizzards, height, width)
    print(round)

    # Start to goal
    possible_positions = {start}
    while True:
        update_blizzards(blizzards, height, width)
        possible_positions = find_new_possible_pos(possible_positions, blizzards, height, width)
        round += 1
        if (goal_x, goal_y - 1) in possible_positions:
            break
    round += 1
    print(round)


if __name__ == "__main__":
    main()
