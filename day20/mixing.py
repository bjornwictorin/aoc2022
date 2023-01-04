#!/usr/bin/env python3

from typing import Union

class Node:
    def __init__(self, prev: Union["Node", None], next: Union["Node", None], index: int, value: int):
        self.prev = prev
        self.next = next
        self.index = index
        self.value = value
    
    def __str__(self):
        return str(self.value)


def parse_input(file_name: str) -> Node:
    base_node = None
    last_node = None
    with open(file_name, "r") as f:
        for ii, line in enumerate(f):
            if ii == 0:
                base_node = Node(None, None, ii, int(line))
                last_node = base_node
            else:
                new_node = Node(last_node, base_node, ii, int(line))
                assert(isinstance(base_node, Node))
                assert(isinstance(last_node, Node))
                base_node.prev = new_node
                last_node.next = new_node
                last_node = new_node
    assert(isinstance(base_node, Node))
    return base_node


def print_list(base_node: Node) -> None:
    print_node = base_node
    assert(isinstance(print_node, Node))
    print(f"{print_node}, ", end = "")
    print_node = print_node.next
    while print_node != base_node:
        print(f"{print_node}, ", end = "")
        assert(isinstance(print_node, Node))
        print_node = print_node.next
    print()


def list_len(base_node: Node) -> int:
    entries = 1
    next_node = base_node.next
    while next_node != base_node:
        entries += 1
        assert(isinstance(next_node, Node))
        next_node = next_node.next
    return entries


def find_node(base_node: Node, index: int) -> Node:
    if base_node.index == index:
        return base_node
    node = base_node.next
    while node != base_node:
        if node.index == index:
            return node
        node = node.next
    assert False


def find_node_by_value(base_node: Node, value: int) -> Node:
    if base_node.value == value:
        return base_node
    node = base_node.next
    while node != base_node:
        if node.value == value:
            return node
        node = node.next
    assert False


def move_forward(base_node: Node) -> None:
    next_node = base_node.next
    next_next_node = next_node.next
    prev_node = base_node.prev
    # remove base
    prev_node.next = next_node
    next_node.prev = prev_node
    # insert at new pos
    next_node.next = base_node
    next_next_node.prev = base_node
    base_node.prev = next_node
    base_node.next = next_next_node


def move_backward(base_node: Node) -> None:
    next_node = base_node.next
    prev_node = base_node.prev
    prev_prev_node = prev_node.prev
    # remove base
    prev_node.next = next_node
    next_node.prev = prev_node
    # insert at new pos
    prev_node.prev = base_node
    prev_prev_node.next = base_node
    base_node.prev = prev_prev_node
    base_node.next = prev_node


def mix_list(base_node: Node) -> None:
    num_entries = list_len(base_node)
    for ii in range(num_entries):
        node_to_move = find_node(base_node, ii)
        steps = node_to_move.value
        if steps > 0:
            for _ in range(steps):
                move_forward(node_to_move)
        elif steps < 0:
            for _ in range(-steps):
                move_backward(node_to_move)


def calc_code(base_node: Node) -> int:
    code = 0
    zero_node = find_node_by_value(base_node, 0)
    num_entries = list_len(base_node)
    steps = 1000 % num_entries
    code_node = zero_node
    for ii in range(3):
        for _ in range(steps):
            code_node = code_node.next
        code += code_node.value
    return code


def main():
    base_node = parse_input("input.txt")
    mix_list(base_node)
    code = calc_code(base_node)
    print(code)


if __name__ == "__main__":
    main()

