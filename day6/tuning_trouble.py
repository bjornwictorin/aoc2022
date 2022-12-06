#!/usr/bin/env python3


def all_unique(sequence: str) -> bool:
    return len(set(sequence)) == len(sequence)


def find_first_pos(line: str) -> int:
    for pos in range(4, len(line)):
        four_latest = line[pos - 4 : pos]
        assert len(four_latest) == 4
        if all_unique(four_latest):
            return pos
    return -1


def main():
    with open("input.txt", "r") as f:
        for line in f:
            pos = find_first_pos(line)
            assert pos != -1
            print(pos)


if __name__ == "__main__":
    main()
