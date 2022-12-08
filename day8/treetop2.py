#!/usr/bin/env python3

from typing import Tuple


def first_blocker(tree: int, tree_line: Tuple[int, ...]) -> int:
    for index, other_tree in enumerate(tree_line):
        if other_tree >= tree:
            return index + 1
    return len(tree_line)


def calc_scenic_score(x: int, y: int, forest: Tuple[Tuple[int, ...]]) -> int:
    tree = int(forest[y][x])
    trees_left_list = list(forest[y][: x])
    trees_left_list.reverse()
    trees_left = tuple(trees_left_list)
    trees_right = tuple(forest[y][x + 1 :])
    trees_above = tuple(forest[ii][x] for ii in range(y - 1, -1, -1))
    trees_below = tuple(forest[ii][x] for ii in range(y + 1, len(forest[0])))
    scenic_score = first_blocker(tree, trees_left)
    scenic_score *= first_blocker(tree, trees_right)
    scenic_score *= first_blocker(tree, trees_above)
    scenic_score *= first_blocker(tree, trees_below)
    return scenic_score



def main():
    f = open("input.txt", "r")
    # Create tuple of tuples of ints for all input
    forest = tuple(tuple(int(jj) for jj in (ii.strip())) for ii in f.readlines())
    max_scenic_score = 0
    # Edges can be skipped because anything multiplied with zero is zero
    for y in range(1, len(forest) - 1):
        for x in range(1, len(forest[0]) - 1):
            max_scenic_score = max(calc_scenic_score(x, y, forest), max_scenic_score)
    print(max_scenic_score)


if __name__ == "__main__":
    main()
