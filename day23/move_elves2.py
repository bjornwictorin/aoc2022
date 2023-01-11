#!/usr/bin/env python3

from typing import Dict, Tuple, Set

def parse_input(file_name: str) -> Set[Tuple[int, int]]:
    elf_set = set()
    with open(file_name, "r") as f:
        for row, line in enumerate(f):
            for col, symbol in enumerate(line):
                if symbol == "#":
                    elf_set.add((col, row))
    return elf_set


def print_elves(elf_set: Set[Tuple[int, int]]) -> int:
    empty_tiles = 0
    min_x = min(elf_set)[0] # Tuples sorted by first member by default
    min_y = min(elf_set, key=lambda coord: coord[1])[1]
    max_x = max(elf_set)[0] # Tuples sorted by first member by default
    max_y = max(elf_set, key=lambda coord: coord[1])[1]
    for yy in range(min_y, max_y + 1):
        for xx in range(min_x, max_x + 1):
            if (xx, yy) in elf_set:
                print("#", end = "")
            else:
                empty_tiles += 1
                print(".", end = "")
        print()
    print()
    return empty_tiles


def has_neighbors(elf: Tuple[int, int], elf_set: Set[Tuple[int, int]]) -> bool:
    for yy in (elf[1] - 1, elf[1], elf[1] + 1):
        for xx in (elf[0] - 1, elf[0], elf[0] + 1):
            coord = (xx, yy)
            if coord == (elf[0], elf[1]):
                continue
            if coord in elf_set:
                return True
    return False


def tiles_are_empty(pos_a: Tuple[int, int], pos_b: Tuple[int, int], pos_c: Tuple[int, int], elf_set: Set[Tuple[int, int]]) -> bool:
    return (pos_a not in elf_set) and (pos_b not in elf_set) and (pos_c not in elf_set)


def move_direction(direction: int, elf: Tuple[int, int], elf_set: Set[Tuple[int, int]]):
    new_pos = (elf[0], elf[1])
    if direction == 0 and tiles_are_empty((elf[0] - 1, elf[1] - 1), (elf[0], elf[1] - 1), (elf[0] + 1, elf[1] - 1), elf_set):
        # North
        new_pos = (elf[0], elf[1] - 1)
    elif direction == 1 and tiles_are_empty((elf[0] - 1, elf[1] + 1), (elf[0], elf[1] + 1), (elf[0] + 1, elf[1] + 1), elf_set):
        # South
        new_pos = (elf[0], elf[1] + 1)
    elif direction == 2 and tiles_are_empty((elf[0] - 1, elf[1] - 1), (elf[0] - 1, elf[1]), (elf[0] - 1, elf[1] + 1), elf_set):
        # West
        new_pos = (elf[0] - 1, elf[1])
    elif direction == 3 and tiles_are_empty((elf[0] + 1, elf[1] - 1), (elf[0] + 1, elf[1]), (elf[0] + 1, elf[1] + 1), elf_set):
        # East
        new_pos = (elf[0] + 1, elf[1])
    return new_pos


def find_new_positions(elf_set: Set[Tuple[int, int]], round: int) -> Dict[Tuple[int, int], Tuple[int, int]]:
    elves_to_move = {}
    for elf in elf_set:
        if not has_neighbors(elf, elf_set):
            continue
        for ii in range(4):
            new_pos = move_direction((round + ii) % 4, elf, elf_set)
            if new_pos != elf:
                elves_to_move[elf] = new_pos
                break
    return elves_to_move


def handle_collisions(elves_to_move: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
    already_seen_coordinates = set()
    collisions = set()
    # Detect collisions
    for new_pos in elves_to_move.values():
        if new_pos in already_seen_coordinates:
            #elves_to_move[old_pos] = old_pos
            collisions.add(new_pos)
        already_seen_coordinates.add(new_pos)
    # Cancel collisions
    for old_pos, new_pos in elves_to_move.items():
        if new_pos in collisions:
            elves_to_move[old_pos] = old_pos


def update_positions(elf_set: Set[Tuple[int, int]], elves_to_move: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
    for old_pos, new_pos in elves_to_move.items():
        elf_set.remove(old_pos)
        elf_set.add(new_pos)


def main():
    elf_set = parse_input("input.txt")
    print("Initial state")
    print_elves(elf_set)
    round = 0
    while True:
        elves_to_move = find_new_positions(elf_set, round)
        if not elves_to_move:
            # Break if empty
            break
        handle_collisions(elves_to_move)
        update_positions(elf_set, elves_to_move)
        round += 1
    print(round + 1)
    print_elves(elf_set)


if __name__ == "__main__":
    main()
