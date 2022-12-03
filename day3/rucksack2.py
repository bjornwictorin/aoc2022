#!/usr/bin/env python3


from linecache import getlines
from typing import Tuple


def get_item_value(item: str) -> int:
    assert len(item) == 1
    assert item.isalpha()
    lowercase_alphabet = "abcdefghijklmnopqrstuvwxyz"
    assert len(lowercase_alphabet) == 26
    value = 0
    if item.islower():
        value = lowercase_alphabet.find(item) + 1
    else:
        value = lowercase_alphabet.find(item.lower()) + 1 + 26
    return value


def find_group_badge(elf_group: Tuple[str, str, str]) -> str:
    assert len(elf_group) == 3
    badge = ""
    for item in elf_group[0]:
        if item in elf_group[1] and item in elf_group[2]:
            badge = item
            break
    assert len(badge) == 1
    return badge


def main():
    prio_sum = 0
    all_rucksacks = [ii.strip() for ii in getlines("input.txt")]
    num_rucksacks = len(all_rucksacks)
    assert num_rucksacks % 3 == 0
    for ii in range(0, num_rucksacks, 3):
        elf_group = (all_rucksacks[ii], all_rucksacks[ii + 1], all_rucksacks[ii + 2])
        badge = find_group_badge(elf_group)
        prio_sum += get_item_value(badge)
    print(prio_sum)


if __name__ == "__main__":
    main()
