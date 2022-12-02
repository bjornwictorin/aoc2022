#!/usr/bin/env python3

def get_shape_points(shape: str) -> int:
    if shape == "X":
        return 1
    elif shape == "Y":
        return 2
    elif shape == "Z":
        return 3
    else:
        assert False, "Only X, Y, and Z are valid shapes"


def remap_shape(shape_abc: str) -> str:
    shape_xyz = ""
    if shape_abc == "A":
        shape_xyz = "X"
    elif shape_abc == "B":
        shape_xyz = "Y"
    elif shape_abc == "C":
        shape_xyz = "Z"
    else:
        assert False
    return shape_xyz


def get_result_points(my_shape: str, their_shape: str) -> int:
    result_points = 0
    if my_shape == their_shape:
        result_points = 3
    elif my_shape == "X": # rock
        if their_shape == "Y": # paper
            result_points = 0 # loss
        elif their_shape == "Z": # scissors
            result_points = 6 # win
        else:
            assert False
    elif my_shape == "Y": # paper
        if their_shape == "X": # rock
            result_points = 6 # win
        elif their_shape == "Z": # scissors
            result_points = 0 # loss
        else:
            assert False
    elif my_shape == "Z": # scissors
        if their_shape == "X": # rock
            result_points = 0 # loss
        elif their_shape == "Y": # paper
            result_points = 6 # win
        else:
            assert False
    return result_points
    


def main():
    points = 0
    with open("input.txt", "r") as f:
        for line in f:
            their_shape, my_shape = line.strip().split(" ")
            points += get_shape_points(my_shape)
            points += get_result_points(my_shape, remap_shape(their_shape))
    print(points)


if __name__ == "__main__":
    main()
