#!/usr/bin/env python3


def all_unique(sequence: str) -> bool:
    return len(set(sequence)) == len(sequence)


def find_first_pos(line: str, num_unique_chars: int) -> int:
    for pos in range(num_unique_chars, len(line)):
        four_latest = line[pos-num_unique_chars:pos]
        assert len(four_latest) == num_unique_chars
        if all_unique(four_latest):
            return pos
    return -1

def main():
    with open("input.txt", "r") as f:
        for line in f:
            pos = find_first_pos(line, 14)
            assert(pos != -1)
            print(pos)


if __name__ == "__main__":
    main()
