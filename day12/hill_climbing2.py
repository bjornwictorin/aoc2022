#!/usr/bin/env python3

import queue

from typing import List, Tuple, Set


HILL_MAP: List[List[int]] = []
WIDTH = 0
HEIGHT = 0
GOAL = (0, 0)

def find_char(char: int) -> Tuple[int, int]:
    pos = (-1, -1)
    for y, line in enumerate(HILL_MAP):
        if char in line:
            pos = (line.index(char), y)
    assert pos != (-1, -1), f"Error: {char} not found!"
    return pos
            

def find_start() -> Tuple[int, int]:
    return find_char(ord("S"))


def find_end() -> Tuple[int, int]:
    return find_char(ord("E"))

def set_start_and_goal_val(start: Tuple[int, int], goal: Tuple[int, int]) -> None:
    start_x, start_y = start
    goal_x, goal_y = goal
    HILL_MAP[start_y][start_x] = ord("a")
    HILL_MAP[goal_y][goal_x] = ord("z")


def reachable(pos: Tuple[int, int], next_pos: Tuple[int, int]) -> bool:
    x, y = pos
    next_x, next_y = next_pos
    height = len(HILL_MAP)
    width = len(HILL_MAP[0])
    if (next_x < 0) or (next_y < 0) or (next_x >= width) or (next_y >= height) or (HILL_MAP[next_y][next_x] < (HILL_MAP[y][x] - 1)):
        return False
    else:
        return True
    

def breadth_first_search(start: Tuple[int, int]) -> int:
    # queue.Queue is a FIFO
    nodes_to_visit: queue.Queue[Tuple[Tuple[int, int], int]] = queue.Queue()
    nodes_to_visit.put((start, 0))
    visited_nodes: Set[Tuple[int, int]] = set()
    visited_nodes.add(start)
    while not nodes_to_visit.empty():
        node = nodes_to_visit.get()
        (x, y), steps = node
        node_above = (x, y - 1)
        node_right = (x + 1, y)
        node_below = (x, y + 1)
        node_left = (x - 1, y)
        for neighbour in (node_above, node_right, node_below, node_left):
            if reachable((x, y), neighbour) and neighbour not in visited_nodes:
                # if neighbour == GOAL:
                next_x, next_y = neighbour
                if HILL_MAP[next_y][next_x] == ord("a"):
                    return steps + 1
                nodes_to_visit.put((neighbour, steps + 1))
                visited_nodes.add(neighbour)
    assert False, "Error, goal should have been reached."
    return -1


def main():
    global HILL_MAP
    global WIDTH
    global HEIGHT
    global GOAL
    with open("input.txt", "r") as f:
        for line in f:
            HILL_MAP.append([ord(ii) for ii in [*line.strip()]])
    WIDTH = len(HILL_MAP[0])
    HEIGHT = len(HILL_MAP)
    start = find_start()
    GOAL = find_end()
    set_start_and_goal_val(start, GOAL)
    min_steps = breadth_first_search(GOAL)
    assert min_steps != -1
    print(min_steps)


if __name__ == "__main__":
    main()
