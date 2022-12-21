#!/usr/bin/env python3

from typing import Tuple, Set

import queue


def reaches_water(start_cube: Tuple[int, int, int], max_xyz: Tuple[int, int, int], stone_cubes: Set[Tuple[int, int, int]]) -> bool:
    """Use BFS to see if cube touches wates"""
    # queue.Queue is a FIFO
    nodes_to_visit: queue.Queue[Tuple[int, int, int]] = queue.Queue()
    nodes_to_visit.put(start_cube)
    visited_nodes: Set[Tuple[int, int, int]] = set()
    visited_nodes.add(start_cube)
    while not nodes_to_visit.empty():
        node = nodes_to_visit.get()
        x, y, z = node
        nb0 = (x + 1, y, z)
        nb1 = (x - 1, y, z)
        nb2 = (x, y + 1, z)
        nb3 = (x, y - 1, z)
        nb4 = (x, y, z + 1)
        nb5 = (x, y, z -  1)
        for nb in (nb0, nb1, nb2, nb3, nb4, nb5):
            if (nb not in stone_cubes) and (nb not in visited_nodes):
                for ii, dim in enumerate(nb):
                    if dim < 0 or dim > max_xyz[ii]:
                        return True
                nodes_to_visit.put(nb)
                visited_nodes.add(nb)
    return False


def main():
    cubes = set()
    max_x = 0
    max_y = 0
    max_z = 0
    with open("input.txt", "r") as f:
        for line in f:
            x, y, z = [int(ii) for ii in line.split(",")]
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)
            cubes.add((x, y, z))
    surface_area = 0
    for cube in cubes:
        area = 0
        x, y, z = cube
        for neighbour in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if (neighbour not in cubes) and reaches_water(neighbour, (max_x, max_y, max_z), cubes):
                area += 1
        surface_area += area
    print(surface_area)

if __name__ == "__main__":
    main()
