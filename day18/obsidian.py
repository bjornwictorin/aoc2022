#!/usr/bin/env python3


def main():
    cubes = set()
    with open("input.txt", "r") as f:
        for line in f:
            x, y, z = [int(ii) for ii in line.split(",")]
            cubes.add((x, y, z))
    # print(cubes)
    surface_area = 0
    for cube in cubes:
        area = 6
        x, y, z = cube
        if (x + 1, y, z) in cubes:
            area -= 1
        if (x - 1, y, z) in cubes:
            area -= 1
        if (x, y + 1, z) in cubes:
            area -= 1
        if (x, y - 1, z) in cubes:
            area -= 1
        if (x, y, z + 1) in cubes:
            area -= 1
        if (x, y, z - 1) in cubes:
            area -= 1
        surface_area += area
    print(surface_area)

if __name__ == "__main__":
    main()
