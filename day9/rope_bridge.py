#!/usr/bin/env python3

from typing import Tuple


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
        tail_pos = (head_x - 1, head_y)
    elif x_dist == -2:
        tail_pos = (head_x + 1, head_y)
    # y pos
    elif y_dist == 2:
        tail_pos = (head_x, head_y - 1)
    elif y_dist == -2:
        tail_pos = (head_x, head_y + 1)
    else:
        assert abs(x_dist < 2) and abs(y_dist < 2)
    return tail_pos


def main():
    head_pos = (0,0)
    tail_pos = (0,0)
    all_tail_pos = set()
    all_tail_pos.add(tail_pos)
    with open("input.txt", "r") as f:
        for line in f:
            direction, steps_str = line.strip().split(" ")
            steps = int(steps_str)
            for _ in range(steps):
                head_pos = move_head(head_pos, direction)
                tail_pos = move_tail(head_pos, tail_pos)
                all_tail_pos.add(tail_pos)
    print(len(all_tail_pos))


if __name__ == "__main__":
    main()
