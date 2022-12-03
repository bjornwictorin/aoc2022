#!/usr/bin/env python3


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


def main():
    prio_sum = 0
    with open("input.txt", "r") as f:
        for line in f:
            line = line.strip()
            num_items = len(line)
            assert num_items % 2 == 0
            first_half = line[:num_items//2]
            second_half = line[num_items//2:]
            assert len(first_half) == len(second_half)
            for item in set(first_half): # convert to set to only check each letter once
                if item in second_half:
                    value = get_item_value(item)
                    prio_sum += value
    print(prio_sum)


if __name__ == "__main__":
    main()
