#!/usr/bin/env python3


from typing import Tuple, List


def init_stacks(file_name) -> Tuple[List[str], ...]:
    """
    Read the first part of the input file,
    which defines the initial state of the crate stacks.
    """
    with open(file_name, "r") as f:
        line = f.readline()
        assert "[" in line
        assert "]" in line
        num_stacks = len(line) // 4
        stacks = []
        for ii in range(num_stacks):
            stacks.append([])
        stacks = tuple(stacks)
        while "[" in line:
            for index, char_pos in enumerate(range(1, 4 * num_stacks, 4)):
                crate_content = line[char_pos]
                if crate_content.isalpha():
                    stacks[index].append(crate_content)
            line = f.readline()
        # assert len(stacks[0]) == 2, f"Expected len: 2, actual len: {len(stacks[0])}"
        # assert len(stacks[1]) == 3, f"Expected len: 3, actual len: {len(stacks[1])}"
        # assert len(stacks[2]) == 1, f"Expected len: 1, actual len: {len(stacks[2])}"
        # All stacks were read from top to bottom
        # and must be flipped
        for index, _ in enumerate(stacks):
            stacks[index].reverse()
        return stacks


def decode_move_instr(line: str) -> Tuple[int, int, int]:
    line_parts = line.split(" ")
    assert len(line_parts) == 6
    num_crates = int(line_parts[1])
    from_stack = int(line_parts[3])
    to_stack = int(line_parts[5])
    return num_crates, from_stack, to_stack


def move_n_crates(stacks: Tuple[List[str], ...], num_crates: int, from_stack: int, to_stack: int) -> None:
    crates_to_move = []
    for _ in range(num_crates):
        assert len(stacks[from_stack - 1]) > 0, "From stack must not be empty!"
        # Take indices -1 because indexing is from 0, not 1
        crate_content = stacks[from_stack - 1].pop()
        crates_to_move.append(crate_content)
    for _ in range(num_crates):
        crate_content = crates_to_move.pop()
        stacks[to_stack - 1].append(crate_content)
    assert len(crates_to_move) == 0


def move_stacks(stacks: Tuple[List[str], ...], file_name: str) -> None:
    with open(file_name, "r") as f:
        for line in f:
            if line[0] == "m":
                num_crates, from_stack, to_stack = decode_move_instr(line)
                move_n_crates(stacks, num_crates, from_stack, to_stack)


def get_top_crates(stacks: Tuple[List[str], ...]) -> str:
    sequence = ""
    for stack in stacks:
        if len(stack) > 0:
            sequence += stack[-1]
    return sequence


def main():
    input_file_name = "input.txt"
    stacks = init_stacks(input_file_name)
    move_stacks(stacks, input_file_name)
    top_crates_sequence = get_top_crates(stacks)
    assert len(top_crates_sequence) == len(stacks)
    print(top_crates_sequence)


if __name__ == "__main__":
    main()
