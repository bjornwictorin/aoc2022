#!/usr/bin/env python3

from enum import Enum
from typing import List, Union, Tuple


def parse_int(line: str, pos: int) -> Tuple[int, int]:
    num = 0
    width = 0
    while line[pos].isnumeric():
        num *= 10
        num += int(line[pos])
        pos += 1
        width += 1
    return num, width


def fill_list(signal: List, line: str, line_pos: int) -> int:
    while line_pos < len(line):
        if line[line_pos] == "[":
            signal.append([])
            line_pos = fill_list(signal[-1], line, line_pos + 1)
        elif line[line_pos] == "]":
            return line_pos + 1
        elif line[line_pos].isnumeric():
            num, width = parse_int(line, line_pos)
            line_pos += width
            signal.append(num)
        elif line[line_pos] == "," or line[line_pos] == "\n":
            line_pos += 1
        else:
            assert False, "Lines must only contain numbers, comma, and brackets"
    return line_pos


def parse_signal(line: str, line_pos: int) -> List:
    signal = []
    line_pos = fill_list(signal, line, 0)
    assert line_pos == len(line)
    return signal[0]


class Order(Enum):
    IN_ORDER = 1
    NOT_IN_ORDER = 2
    UNDECIDED = 3


def check_order(left_signal: List[Union[List, int]], right_signal: List[Union[List, int]]) -> Order:
    # print(left_signal)
    # print(right_signal)
    shortest_len = min(len(left_signal), len(right_signal))
    for ii in range(shortest_len):
        s1 = left_signal[ii]
        s2 = right_signal[ii]
        order = Order.UNDECIDED
        if isinstance(s1, int) and isinstance(s2, int):
            if s1 < s2:
                order = Order.IN_ORDER
            elif s1 > s2:
                order = Order.NOT_IN_ORDER
        elif isinstance(s1, list) and isinstance(s2, list):
            order = check_order(s1, s2)
        elif isinstance(s1, int) and isinstance(s2, list):
            order = check_order([s1], s2)
        elif isinstance(s1, list) and isinstance(s2, int):
            order = check_order(s1, [s2])
        if order == Order.IN_ORDER or order == Order.NOT_IN_ORDER:
            return order
    # assert(left_signal[:shortest_len] == right_signal[:shortest_len])
    # Order could not be decided by entries, check length now
    if len(left_signal) < len(right_signal):
        order = Order.IN_ORDER
    elif len(left_signal) > len(right_signal):
        order = Order.NOT_IN_ORDER
    else:
        order = Order.UNDECIDED
    return order


def main():
    # div_packet0 = [[2]]
    # div_packet1 = [[6]]
    div_packets = [[[2]], [[6]]]
    signals = []
    with open("input.txt", "r") as f:
        for line in f:
            if line != "\n":
                signals.append(parse_signal(line, 0))
    # Check the number of packets that [[2]] and [[6]] are bigger than
    # div0_index = 1
    # div1_index = 1
    div_indices = [1, 2]
    for signal in signals:
        for ii in range(2):
            order = check_order(signal, div_packets[ii])
            assert order != Order.UNDECIDED
            if order == Order.IN_ORDER:
                div_indices[ii] += 1
        
    product = div_indices[0] * div_indices[1]
    print(product)

if __name__ == "__main__":
    main()
