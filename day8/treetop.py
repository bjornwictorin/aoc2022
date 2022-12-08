#!/usr/bin/env python3

from typing import Tuple


def is_visible(x: int, y: int, forest: Tuple[Tuple[str, ...]]) -> int:
    tree = int(forest[y][x])
    if tree > max(forest[y][: x]): # from left side
        return True
    elif tree > max(forest[y][x + 1 :]): # from right side
        return True
    elif tree > max((forest[ii][x] for ii in range(y))): # from top
        return True
    elif tree > max((forest[ii][x] for ii in range(y + 1, len(forest[0])))): # from bottom
        return True
    # Not visible from any direction
    return False


def main():
    f = open("input.txt", "r")
    # Create tuple of tuples of ints for all input
    forest = tuple(tuple(int(jj) for jj in (ii.strip())) for ii in f.readlines())
    # Subtract corners because otherwisee they get counted twice
    num_visible_trees = 2 * len(forest) + 2 * len(forest[0]) - 4
    for y in range(1, len(forest) - 1):
        for x in range(1, len(forest[0]) - 1):
            if is_visible(x, y, forest):
                num_visible_trees += 1
    print(num_visible_trees)


if __name__ == "__main__":
    main()
