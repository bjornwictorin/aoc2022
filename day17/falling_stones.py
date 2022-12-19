#!/usr/bin/env python3

from typing import List


# Store all shapes upside down
SHAPE0 = \
""".......
.......
.......
..@@@@.
"""

SHAPE1 = \
""".......
.......
.......
...@...
..@@@..
...@...
"""

SHAPE2 = \
""".......
.......
.......
..@@@..
....@..
....@..
"""

SHAPE3 = \
""".......
.......
.......
..@....
..@....
..@....
..@....
"""


SHAPE4 = \
""".......
.......
.......
..@@...
..@@...
"""

SHAPE_LIST = [SHAPE0, SHAPE1, SHAPE2, SHAPE3, SHAPE4]

def read_input(file_name: str) -> str:
    wind_pattern = ""
    with open(file_name, "r") as f:
        for line in f:
            wind_pattern += line.strip()
    return wind_pattern


def init_rock(room: List[List[str]], index: int) -> int:
    rock = SHAPE_LIST[index]
    rock_height = 0
    # for ii in range(rock_height, 0, -1):
    for line in rock.splitlines():
        room.append([*line.strip()])
        rock_height += 1
    return rock_height - 3


def blocked_right(room: List[List[str]], rock_height: int, rock_top_row: int) -> bool:
    for line in room[rock_top_row - rock_height + 1: rock_top_row + 1]:
        for ii, symbol in enumerate(line):
            if symbol == "@" and (ii == 6 or line[ii + 1] == "#"):
                return True
    return False


def blocked_left(room: List[List[str]], rock_height: int, rock_top_row: int) -> bool:
    for line in room[rock_top_row - rock_height + 1: rock_top_row + 1]:
        for ii, symbol in enumerate(line):
            if symbol == "@" and (ii == 0 or line[ii - 1] == "#"):
                return True
    return False


def move_rock_right(room: List[List[str]], rock_height: int, rock_top_row: int) -> None:
    for line in room[rock_top_row - rock_height + 1 : rock_top_row + 1]:
        for ii in range(5, -1, -1):
            if line[ii] == "@":
                assert line[ii + 1] != "@"
                line[ii + 1] = "@"
                line[ii] = "."


def move_rock_left(room: List[List[str]], rock_height: int, rock_top_row: int) -> None:
    for line in room[rock_top_row - rock_height + 1 : rock_top_row + 1]:
        for ii in range(1, 7):
            if line[ii] == "@":
                assert line[ii - 1] != "@"
                line[ii - 1] = "@"
                line[ii] = "."


def move_rock_sideways(room: List[List[str]], wind_dir: str, rock_height: int, rock_top_row: int) -> None:
    assert wind_dir == "<" or wind_dir == ">", "Invalid wind"
    if wind_dir == ">" and not blocked_right(room, rock_height, rock_top_row):
        move_rock_right(room, rock_height, rock_top_row)
    elif wind_dir == "<" and not blocked_left(room, rock_height, rock_top_row):
        move_rock_left(room, rock_height, rock_top_row)
        

def check_rock_at_rest(room: List[List[str]], rock_height: int, rock_top_row: int) -> bool:
    if len(room) == rock_height:
        return True
    for ii in range(rock_top_row + 1 - rock_height, rock_top_row + 1):
        for jj in range(7):
            if room[ii][jj] == "@" and room[ii - 1][jj] == "#":
                return True
    return False


"""Update @ to # for still stones"""
def change_at_to_hash(room: List[List[str]], rock_height: int, rock_top_row: int) -> None:
    for line in room[rock_top_row - rock_height + 1 : rock_top_row + 1]:
        for ii in range(len(line)):
            if line[ii] == "@":
                line[ii] = "#"


def move_rock_down(room: List[List[str]], rock_height: int, rock_top_row: int) -> bool:
    if check_rock_at_rest(room, rock_height, rock_top_row):
        change_at_to_hash(room, rock_height, rock_top_row)
        return False
    for ii in range(rock_top_row - rock_height, rock_top_row):
        for jj in range(7):
            if room[ii + 1][jj] == "@":
                assert room[ii][jj] == "."
                room[ii][jj] = "@"
                room[ii + 1][jj] = "."
    if room[-1] == [*"......."]:
        room.pop()
    return True


def print_room(room: List[List[str]]) -> None:
    for ii in range(len(room) - 1, -1, -1):
        print("".join(room[ii]))
    print(7 * "-")


def main():
    room: List[List[str]] = []
    wind_pattern = read_input("input.txt")
    num_rocks = 2022
    wind_index = 0
    for ii in range(num_rocks):
        rock_height = init_rock(room, ii % 5)
        rock_top_row = len(room) - 1
        move_rock_sideways(room, wind_pattern[wind_index % len(wind_pattern)], rock_height, rock_top_row)
        wind_index += 1
        while move_rock_down(room, rock_height, rock_top_row):
            rock_top_row -= 1
            move_rock_sideways(room, wind_pattern[wind_index % len(wind_pattern)], rock_height, rock_top_row)
            wind_index += 1
        # print_room(room)
    print(len(room))


if __name__ == "__main__":
    main()
