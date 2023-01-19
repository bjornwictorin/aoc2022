#!/usr/bin/env python3

def main():
    init_seq = [8, 5, 7, 10, 7, 10, 7, 6, 6, 8, 5, 7, 8, 8, 7, 11, 9, 6, 8]
    repeat_seq = [6, 10, 8, 4, 7, 8, 8, 11, 4, 12, 9, 9, 12, 9, 6, 10, 9, 11, 9, 5, 7, 9, 10, 10, 8, 10, 10, 6, 6, 10, 7, 5, 8, 9, 3, 8, 10, 9, 11, 5, 5, 7, 7, 10, 5, 9, 9, 7, 11, 6, 11, 9, 7, 5, 7, 8, 10, 11, 4, 10, 9, 9, 7, 4, 10, 2, 6, 7, 10, 10, 9, 9, 5, 5, 5, 7, 7, 8, 10, 7, 8, 7, 7, 9, 5, 5, 7, 8, 8, 8, 9, 9, 8, 8, 9, 5, 7, 9, 8, 6, 13, 6, 11, 9, 10, 3, 7, 7, 6, 7, 10, 9, 7, 8, 10, 9, 8, 9, 6, 7, 8, 9, 11, 11, 13, 9, 8, 8, 6, 6, 9, 6, 8, 5, 8, 8, 10, 6, 8, 9, 10, 10, 11, 10, 7, 6, 7, 11, 12, 8, 10, 9, 9, 8, 11, 7, 11, 8, 10, 7, 6, 11, 6, 11, 6, 8, 10, 8, 7, 6, 6, 6, 10, 7, 6, 9, 6, 10, 3, 9, 4, 10, 5, 10, 8, 5, 9, 7, 10, 7, 10, 11, 9, 11, 6, 9, 9, 10, 7, 9, 5, 9, 10, 8, 11, 7, 8, 7, 8, 7, 9, 9, 3, 6, 5, 6, 5, 7, 7, 9, 7, 8, 10, 11, 7, 6, 7, 11, 8, 7, 6, 6, 6, 5, 6, 5, 9, 9, 11, 11, 12, 3, 13, 4, 9, 5, 6, 7, 8, 9, 8, 9, 9, 10, 4, 6, 7, 9, 6, 11, 7, 9, 9, 11, 6, 11, 11, 8, 7, 11, 7, 4, 8, 8, 11, 3, 7, 7, 8, 5, 8, 7, 7, 7, 7, 9, 5, 5, 8, 10, 8, 3, 8, 7, 3, 4, 7, 7, 8, 8, 7, 9, 7, 7, 7, 6, 9, 7, 6, 7, 13, 8, 8, 5, 6, 8, 10, 9, 6, 8, 11, 8, 8, 7, 6, 11, 4, 10, 5, 8, 9, 9, 9, 6, 7, 9, 9, 5, 8, 6, 5, 7, 11, 7, 8, 3, 11]
    # Multiply by 5 because each group contains 5 stones
    len_init_seq = 5 * len(init_seq)
    height_init_seq = sum(init_seq)
    print(f"len(init_seq): {5 * len(init_seq)}")
    print(f"height(init_seq): {sum(init_seq)}")

    len_repeat_seq = 5 * len(repeat_seq)
    height_repeat_seq = sum(repeat_seq)
    print(f"len(repeat_seq): {5 * len(repeat_seq)}")
    print(f"height(repeat_seq): {sum(repeat_seq)}")

    num_repeats = 1000000000000//(5 * len(repeat_seq))
    elements_not_in_repeats = 1000000000000%(5 * len(repeat_seq))
    print(f"1000000000000 // {(5 * len(repeat_seq))} = {1000000000000//(5 * len(repeat_seq))}")
    print(f"1000000000000 % {(5 * len(repeat_seq))} = {1000000000000%(5 * len(repeat_seq))}")

    assert elements_not_in_repeats >= len_init_seq
    height = height_init_seq + num_repeats * height_repeat_seq + sum(repeat_seq[:(elements_not_in_repeats - len_init_seq)//5])
    print(height)


if __name__ == "__main__":
    main()
