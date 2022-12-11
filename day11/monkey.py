#!/usr/bin/env python3

from audioop import reverse
from typing import List
import re

class Monkey():
    def __init__(self, items, op_type, op_amount, test_divisor, monkey_if_true, monkey_if_false):
        self.items: List[int] = items
        self.op_type: str = op_type
        self.op_amount: str = op_amount
        self.test_divisor: int = test_divisor
        self.monkey_if_true: Monkey = monkey_if_true
        self.monkey_if_false: Monkey = monkey_if_false
        self.num_insp = 0

    def __str__(self) -> str:
        return self.items.__str__()
    
    def apply_op(self, item: int) -> int:
        op_amount = item if self.op_amount == "old" else int(self.op_amount)
        if self.op_type == "*":
            item = item * op_amount
        elif self.op_type == "+":
            item = item + op_amount
        else:
            assert False, "Only + and * are allowed operations"
        return item
    
    def test_item(self, item: int):
        return item % self.test_divisor == 0


    def play(self, monkey_list: List["Monkey"]):
        for item in self.items:
            item = self.apply_op(item)
            item = item // 3
            if self.test_item(item):
                monkey_list[self.monkey_if_true].items.append(item)
            else:
                monkey_list[self.monkey_if_false].items.append(item)
        self.num_insp += len(self.items)
        self.items.clear()

    

def parse_input(file_name: str) -> List[Monkey]:
    monkey_list = []
    with open(file_name, "r") as f:
        for line in f:
            if line.startswith("  Starting items:"):
                item_list_str = re.split(": |, ", line)
                items = [int(item) for item in item_list_str[1:]]
            elif line.startswith("  Operation:"):
                operation_str = re.split(" = ", line)[1]
                operations_str_parts = re.split(" ", operation_str)
                assert operations_str_parts[0] == "old", f"actual: {operations_str_parts}"
                op_type = operations_str_parts[1]
                op_amount = operations_str_parts[2].strip()
                #print(op_type + " " + op_amount)
            elif line.startswith("  Test:"):
                test_divisor = int(line.split()[-1])
                #print(test_divisor)
            elif line.startswith("    If true:"):
                monkey_if_true = int(line.split()[-1])
                #print(monkey_if_true)
            elif line.startswith("    If false:"):
                monkey_if_false = int(line.split()[-1])
                #print(monkey_if_false)
                monkey_list.append(Monkey(items, op_type, op_amount, test_divisor, monkey_if_true, monkey_if_false))
    return monkey_list


def print_state(monkey_list: List[Monkey], round) -> None:
    print(f"After round {round + 1}:")
    for ii, monkey in enumerate(monkey_list):
        print(f"Monkey {ii}: {monkey}")


def get_num_insp(monkey_list: List[Monkey]) -> List[int]:
    num_inspections = []
    for monkey in monkey_list:
        num_inspections.append(monkey.num_insp)
    return num_inspections


def main():
    monkey_list = parse_input("input.txt")
    for round in range(20):
        for monkey in monkey_list:
            monkey.play(monkey_list)
        #print_state(monkey_list, round)
    num_inspections = get_num_insp(monkey_list)
    num_inspections.sort()
    mb_level = num_inspections[-2] * num_inspections[-1]
    print(mb_level)
    

if __name__ == "__main__":
    main()
