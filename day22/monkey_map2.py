#!/usr/bin/env python3

import copy
from typing import List, Tuple, Union

def find_max_len(file_name: str) -> int:
    max_len = 0
    with open(file_name, "r") as f:
        for line in f:
            max_len = max(len(line.strip()), max_len)
    return max_len


def read_map(file_name: str) -> Tuple[List[str], str]:
    area_map = []
    sequence_str = ""
    max_len = find_max_len(file_name)
    with open(file_name, "r") as f:
        for line in f:
            if line[0] in (" ", ".", "#"):
                assert "." in line
                area_map.append(line.rstrip() + ((max_len - len(line.strip())) * " ")) # remove newline characters and pad width
            elif len(line) > 1:
                sequence_str = line
    return area_map, sequence_str


def split_sequence(sequence_str: str) -> List[Union[int, str]]:
    sequence = []
    int_accumulator = 0
    for char in sequence_str:
        if char.isnumeric():
            int_accumulator *= 10
            int_accumulator += int(char)
        else:
            if int_accumulator != 0:
                sequence.append(int_accumulator)
                int_accumulator = 0
            if char == "R" or char == "L":
                sequence.append(char)
            else:
                assert char == "\n", f"Invalid character: {char}"
    return sequence


def get_start_pos(area_map: List[str]) -> Tuple[int, int, int]:
    col = area_map[0].find(".")
    return (0, col, 0)


def go_right(pos: Tuple[int, int, int], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    old_row = row
    side_len = len(area_map) // 4
    if col == len(area_map[row]) - 1 or area_map[row][col + 1] == " ":
        # Going over the edge on the right side
        if 0 <= row < side_len:
            row = 3 * side_len - 1 - row
            col = 2 * side_len - 1
            dir = 2
        elif side_len <= row < 2 * side_len:
            row = side_len - 1
            col = 2 * side_len + (old_row - side_len)
            dir = 3
        elif 2 * side_len <= row < 3 * side_len:
            row = 3 * side_len - 1 - row
            col = 3 * side_len - 1
            dir = 2
        elif 3 * side_len <= row < 4 * side_len:
            row = 3 * side_len - 1
            col = side_len + (old_row - 3 * side_len)
            dir = 3
        else:
            assert False
    else:
        col += 1
    return row, col, dir


def go_left(pos: Tuple[int, int, int], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    old_row = row
    side_len = len(area_map) // 4
    if col == 0 or area_map[row][col - 1] == " ":
        # Going over the edge on the left side
        if 0 <= row < side_len:
            row = 3 * side_len - 1 - row
            col = 0
            dir = 0
        elif side_len <= row < 2 * side_len:
            row = 2 * side_len
            col = old_row - side_len
            dir = 1
        elif 2 * side_len <= row < 3 * side_len:
            row = 3 * side_len - 1 - row
            col = side_len
            dir = 0
        elif 3 * side_len <= row < 4 * side_len:
            row = 0
            col = side_len + old_row - 3 * side_len
            dir = 1
        else:
            assert False
    else:
        col -= 1
    return row, col, dir


def go_down(pos: Tuple[int, int, int], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    old_row = row
    side_len = len(area_map) // 4
    if row == len(area_map) - 1 or area_map[row + 1][col] == " ":
        # Going over the edge on the lower side
        if 0 <= col < side_len:
            row = 0
            # col = 2 * side_len + old_row - 3 * side_len # fel?
            col = 2 * side_len + col
            dir = 1
        elif side_len <= col < 2 * side_len:
            row = 3 * side_len + col - side_len
            col = side_len - 1
            dir = 2
        elif 2 * side_len <= col < 3 * side_len:
            row = side_len + col - 2 * side_len
            col = 2 * side_len - 1
            dir = 2
        else:
            assert False
    else:
        row += 1
    return row, col, dir


def go_up(pos: Tuple[int, int, int], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    side_len = len(area_map) // 4
    if row == 0 or area_map[row - 1][col] == " ":
        # Going over the edge on the upper side
        if 0 <= col < side_len:
            row = side_len + col
            col = side_len
            dir = 0
        elif side_len <= col < 2 * side_len:
            row = 3 * side_len + col - side_len
            col = 0
            dir = 0
        elif 2 * side_len <= col < 3 * side_len:
            row = 4 * side_len - 1
            col = col - 2 * side_len
            dir = 3
        else:
            assert False
    else:
        row -= 1
    return row, col, dir


def predict_next_pos(pos: Tuple[int, int, int], area_map: List[str]) -> Tuple[int, int, int]:
    """Take one step"""
    _, _, dir = pos
    if dir == 0:
        pos = go_right(pos, area_map)
    elif dir == 1:
        pos = go_down(pos, area_map)
    elif dir == 2:
        pos = go_left(pos, area_map)
    elif dir == 3:
        pos = go_up(pos, area_map)
    else:
        assert False
    return pos


def is_wall(pos: Tuple[int, int, int], area_map: List[str]) -> bool:
    row, col, _ = pos
    symbol = area_map[row][col]
    assert symbol != " "
    if symbol == "#":
        return True
    else:
        assert symbol == "."
        return False


def get_new_pos(pos: Tuple[int, int, int], step: Union[int, str], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    arrows = ">v<^"
    if step == "R":
        pos = (row, col, (dir + 1) % 4)
    elif step == "L":
        pos = (row, col, (dir + 4 - 1) % 4)
    else:
        assert isinstance(step, int)
        for _ in range(step):
            next_pos = predict_next_pos(pos, area_map)
            if is_wall(next_pos, area_map):
                break
            else:
                pos = next_pos
    return pos


def calc_pw(pos: Tuple[int, int, int]) -> int:
    row, col, dir = pos
    return 1000 * (row + 1) + 4 * (col + 1) + dir


def main():
    area_map, sequence_str = read_map("input.txt")
    # map_with_route = copy.deepcopy(area_map)
    assert len(area_map) % 4 == 0
    sequence = split_sequence(sequence_str)
    pos: Tuple[int, int, int] = get_start_pos(area_map)
    print(f"start pos: {pos}")
    for step in sequence:
        pos = get_new_pos(pos, step, area_map)
    print(f"pos: {pos}")
    password = calc_pw(pos)
    print(password)


if __name__ == "__main__":
    main()
