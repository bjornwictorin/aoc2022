#!/usr/bin/env python3

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
                area_map.append(line.strip() + ((max_len - len(line.strip())) * " ")) # remove newline characters and pad width
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


def go_right(pos: Tuple[int, int, int], area_map_row: str, step: int) -> Tuple[int, int, int]:
    row, col, dir = pos
    assert dir == 0
    for _ in range(step):
        if col < len(area_map_row) - 1 and area_map_row[col + 1] == "#":
            # wall
            break
        elif col == len(area_map_row) - 1 or area_map_row[col + 1] == " ":
            # wrap
            first_dot = area_map_row.find(".")
            first_hash =  area_map_row.find("#")
            col = first_dot if first_hash == -1 or first_dot < first_hash else col
        elif col < len(area_map_row) - 1 and area_map_row[col + 1] == ".":
            col += 1
    return (row, col, dir)


def go_left(pos: Tuple[int, int, int], area_map_row: str, step: int) -> Tuple[int, int, int]:
    row, col, dir = pos
    assert dir == 2
    for _ in range(step):
        if col > 0 and area_map_row[col - 1] == "#":
            # wall
            break
        elif col == 0 or area_map_row[col - 1] == " ":
            # wrap
            last_dot = area_map_row.rfind(".")
            last_hash =  area_map_row.rfind("#")
            col = last_dot if last_dot > last_hash else col
        elif col > 0 and area_map_row[col - 1] == ".":
            col -= 1
    return (row, col, dir)


def index_in_col(area_map: List[str], col: int, char: str, reverse=False):
    assert len(char) == 1
    assert col < len(area_map[0])
    row = -1
    if reverse:
        for ii in range(len(area_map) - 1, -1, -1):
            line = area_map[ii]
            if line[col] == char:
                row = ii
                break
    else:
        for ii, line in enumerate(area_map):
            if line[col] == char:
                row = ii
                break
    return row


def go_down(pos: Tuple[int, int, int], area_map: List[str], step: int) -> Tuple[int, int, int]:
    row, col, dir = pos
    assert dir == 1
    for _ in range(step):
        if row < len(area_map) - 1 and area_map[row + 1][col] == "#":
            # wall
            break
        elif row == len(area_map) - 1 or area_map[row + 1][col] == " ":
            # wrap
            first_dot = index_in_col(area_map, col, ".")
            first_hash =  index_in_col(area_map, col, "#")
            row = first_dot if first_hash == -1 or first_dot < first_hash else row
        elif row < len(area_map) - 1 and area_map[row + 1][col] == ".":
            row += 1
    return (row, col, dir)


def go_up(pos: Tuple[int, int, int], area_map: List[str], step: int) -> Tuple[int, int, int]:
    row, col, dir = pos
    assert dir == 3
    for _ in range(step):
        if row > 0 and area_map[row - 1][col] == "#":
            # wall
            break
        elif row == 0 or area_map[row - 1][col] == " ":
            # wrap
            last_dot = index_in_col(area_map, col, ".", reverse=True)
            last_hash =  index_in_col(area_map, col, "#", reverse=True)
            row = last_dot if last_dot > last_hash else row
        elif row > 0 and area_map[row - 1][col] == ".":
            row -= 1
    return (row, col, dir)


def get_new_pos(pos: Tuple[int, int, int], step: Union[int, str], area_map: List[str]) -> Tuple[int, int, int]:
    row, col, dir = pos
    if step == "R":
        pos = (row, col, (dir + 1) % 4)
    elif step == "L":
        pos = (row, col, (dir + 4 - 1) % 4)
    else:
        assert isinstance(step, int)
        if dir == 0:
            pos = go_right(pos, area_map[row], step)
        elif dir == 1:
            pos = go_down(pos, area_map, step)
        elif dir == 2:
            pos = go_left(pos, area_map[row], step)
        elif dir == 3:
            pos = go_up(pos, area_map, step)
        else:
            assert False, f"Invalid dir: {dir}"
    return pos


def calc_pw(pos: Tuple[int, int, int]) -> int:
    row, col, dir = pos
    return 1000 * (row + 1) + 4 * (col + 1) + dir


def main():
    area_map, sequence_str = read_map("input.txt")
    sequence = split_sequence(sequence_str)
    pos: Tuple[int, int, int] = get_start_pos(area_map)
    for step in sequence:
        pos = get_new_pos(pos, step, area_map)
    password = calc_pw(pos)
    print(password)


if __name__ == "__main__":
    main()
