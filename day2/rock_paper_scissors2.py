#!/usr/bin/env python3

def get_my_shape(their_shape: str, result: str) -> str:
    my_shape = ""
    if result == "Y": # draw
        my_shape = their_shape
    elif result == "X": # lose
        if their_shape == "A": # rock
            my_shape = "C" # scissors
        elif their_shape == "B": # paper
            my_shape = "A" # rock
        elif their_shape == "C": # scissors
            my_shape = "B" # paper
        else:
            assert False
    elif result == "Z": # win
        if their_shape == "A": # rock
            my_shape = "B"
        elif their_shape == "B": # paper
            my_shape = "C"
        elif their_shape == "C": # scissors
            my_shape = "A"
        else:
            assert False
    else:
        assert False
    assert my_shape != ""
    return my_shape
        

def get_shape_points(shape: str) -> int:
    if shape == "A": # rock
        return 1
    elif shape == "B": # paper
        return 2
    elif shape == "C": # scissors
        return 3
    else:
        assert False, "Only A, B, and C are valid shapes"


def get_result_points(result: str) -> int:
    result_points = 0
    if result == "X": # lose
        result_points = 0
    elif result == "Y": # draw
        result_points = 3
    elif result == "Z": # win
        result_points = 6
    else:
        assert False
    return result_points


def main():
    points = 0
    with open("input.txt", "r") as f:
        for line in f:
            their_shape, result = line.strip().split(" ")
            my_shape = get_my_shape(their_shape, result)
            points += get_shape_points(my_shape)
            points += get_result_points(result)
    print(points)


if __name__ == "__main__":
    main()
