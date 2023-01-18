#!/usr/bin/env python3


def snafu_to_dec(snafu_nbr: str) -> int:
    value = 0
    for char in snafu_nbr:
        # print(f"char: {char}, pos: {pos}")
        value *= 5
        if char == "0":
            pass
        elif char == "1":
            value += 1
        elif char == "2":
            value += 2
        elif char == "-":
            value -= 1
        elif char == "=":
            value -= 2
        else:
            assert False, f"Invalid character: {char}"
    return value


def get_num_digits(dec_nbr: int) -> int:
    num_digits = 0
    range_limit = 0
    while True:
        range_limit += 2 * (5 ** num_digits)
        num_digits += 1
        if abs(dec_nbr) <= range_limit:
            break
    return num_digits


def next_digit(dec_nbr: int, power: int) -> int:
    sign = dec_nbr < 0
    power_five = 5 ** power
    assert abs(dec_nbr) <= (5 ** (power + 1)) // 2
    if abs(dec_nbr) > power_five + (power_five // 2):
        digit = 2
    elif abs(dec_nbr) > (power_five // 2):
        digit = 1
    else:
        digit = 0
    if sign:
        digit = -digit
    return digit


def dec_to_snafu(dec_nbr: int) -> str:
    snafu = ""
    num_digits = get_num_digits(dec_nbr)
    for power in range(num_digits)[::-1]:
        digit = next_digit(dec_nbr, power)
        snafu += "=-012"[digit + 2]
        dec_nbr -= digit * (5 ** power)
    assert dec_nbr == 0
    assert len(snafu) == num_digits
    return snafu


def main():
    total_fuel = 0
    with open("input.txt", "r") as f:
        for line in f:
            total_fuel += snafu_to_dec(line.strip())
    print(dec_to_snafu(total_fuel))


if __name__ == "__main__":
    main()
