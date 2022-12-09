#!/usr/bin/env python3

from typing import Tuple, List


def move_head(head_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    assert len(direction) == 1
    x, y = head_pos
    if direction == "R":
        head_pos = (x + 1, y)
    elif direction == "D":
        head_pos = (x, y - 1)
    elif direction == "L":
        head_pos = (x - 1, y)
    elif direction == "U":
        head_pos = (x, y + 1)
    else:
        assert False, f"Invalid direction: {direction}"
    return head_pos


def move_tail(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> Tuple[int, int]:
    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    x_dist = head_x - tail_x
    y_dist = head_y - tail_y
    # x pos
    if x_dist == 2:
        tail_x += 1
    elif x_dist == -2:
        tail_x -= 1
    # y pos
    if y_dist == 2:
        tail_y += 1
    elif y_dist == -2:
        tail_y -= 1
    assert abs(x_dist < 2) and abs(y_dist < 2)
    return (tail_x, tail_y)

def move_tail(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> Tuple[int, int]:
    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    x_dist = head_x - tail_x
    y_dist = head_y - tail_y
    if (abs(x_dist) + abs(y_dist) == 4):
        tail_x = (head_x + tail_x) // 2
        tail_y = (head_y + tail_y) // 2
        tail_pos = (tail_x, tail_y)
    else:
        # x pos
        if x_dist == 2:
            tail_pos = (head_x - 1, head_y)
        elif x_dist == -2:
            tail_pos = (head_x + 1, head_y)
        # y pos
        elif y_dist == 2:
            tail_pos = (head_x, head_y - 1)
        elif y_dist == -2:
            tail_pos = (head_x, head_y + 1)
    head_x, head_y = head_pos
    tail_x, tail_y = tail_pos
    x_dist = head_x - tail_x
    y_dist = head_y - tail_y
    assert x_dist < 2
    assert y_dist < 2
    return tail_pos


def draw_rope(rope_pos: List[Tuple[int, int]]) -> None:
    x_coords = [ii[0] for ii in rope_pos]
    y_coords = [ii[1] for ii in rope_pos]
    width = max(x_coords) - min(x_coords) + 1
    height = max(y_coords) - min(y_coords) + 1
    area = [["." for x in range(width)] for y in range(height)]
    # Print backwards to get lower indices overwrite lower
    for index in range(len(rope_pos) - 1, -1, -1):
        pos = rope_pos[index]
        map_x = pos[0] - min(x_coords)
        map_y = pos[1] - min(y_coords)
        area[map_y][map_x] = str(index) if index != 0 else "H"
    for line in range(len(area) - 1, -1, -1):
        print(area[line])
    print()


def main():
    num_knots = 10
    rope_pos = [(0,0) for _ in range(num_knots)]
    all_tail_pos = set()
    all_tail_pos.add(rope_pos[-1])
    with open("input.txt", "r") as f:
        for line in f:
            direction, steps_str = line.strip().split(" ")
            steps = int(steps_str)
            for _ in range(steps):
                rope_pos[0] = move_head(rope_pos[0], direction)
                for ii in range(1, num_knots):
                    rope_pos[ii] = move_tail(rope_pos[ii - 1], rope_pos[ii])
                all_tail_pos.add(rope_pos[-1])
                draw_rope(rope_pos)
    print(len(all_tail_pos))


if __name__ == "__main__":
    main()
