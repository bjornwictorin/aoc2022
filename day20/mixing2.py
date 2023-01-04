#!/usr/bin/env python3

from typing import Union


DECRYPTION_KEY = 811589153
NUM_ENTRIES = 0


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
                base_node = Node(None, None, ii, int(line) * DECRYPTION_KEY)
                # * DECRYPTION_KEY
                last_node = base_node
            else:
                new_node = Node(last_node, base_node, ii, int(line) * DECRYPTION_KEY)
                # * DECRYPTION_KEY
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


def remove_entry(base_node: Node) -> None:
    next_node = base_node.next
    prev_node = base_node.prev
    # remove base
    prev_node.next = next_node
    next_node.prev = prev_node


def insert_after(base_node: Node, next_node: Node) -> None:
    # Careful, order matters!
    next_node.next.prev = base_node
    base_node.next = next_node.next
    next_node.next = base_node
    base_node.prev = next_node


def move_forward(base_node: Node, steps: int) -> None:
    remove_entry(base_node)
    next_node = base_node.prev
    # There are NUM_ENTRIES - 1 entries in the list here because base_node is removed
    for _ in range(steps % (NUM_ENTRIES - 1)):
        next_node = next_node.next
    insert_after(base_node, next_node)


def move_backward(base_node: Node, steps: int) -> None:
    remove_entry(base_node)
    prev_node = base_node.next
    # There are NUM_ENTRIES - 1 entries in the list here because base_node is removed
    for _ in range(steps % (NUM_ENTRIES - 1)):
        prev_node = prev_node.prev
    insert_after(base_node, prev_node.prev)


def mix_list(base_node: Node) -> None:
    # num_entries = list_len(base_node)
    for ii in range(NUM_ENTRIES):
        node_to_move = find_node(base_node, ii)
        steps = node_to_move.value
        if steps > 0:
            move_forward(node_to_move, steps)
        elif steps < 0:
            move_backward(node_to_move, -steps)


def calc_code(base_node: Node) -> int:
    code = 0
    zero_node = find_node_by_value(base_node, 0)
    # num_entries = list_len(base_node)
    steps = 1000 % NUM_ENTRIES
    code_node = zero_node
    for ii in range(3):
        for _ in range(steps):
            code_node = code_node.next
        code += code_node.value
    return code


def main():
    base_node = parse_input("input.txt")
    global NUM_ENTRIES
    NUM_ENTRIES = list_len(base_node)
    for _ in range(10):
        mix_list(base_node)
    code = calc_code(base_node)
    print(code)


if __name__ == "__main__":
    main()

