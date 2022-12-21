#!/usr/bin/env python3

from typing import Dict, Tuple


def parse_input(file_name: str, numbers: Dict[str, int], expressions: Dict[str, Tuple[str, str, str]]) -> None:
    with open(file_name, "r") as f:
        for line in f:
            key, value = line.split(": ")
            if value.strip().isnumeric():
                numbers[key] = int(value)
            else:
                lhs, op, rhs = value.strip().split(" ")
                expressions[key] = (lhs, op, rhs)


def calc_expr(expr: Tuple[str, str, str], numbers: Dict[str, int]) -> int:
    lhs, op, rhs = expr
    assert lhs in numbers, "Symbol not calculated"
    assert op in "+-*/", "Invalid op"
    assert rhs in numbers, "Symbol not calculated"
    lhs_val = numbers[lhs]
    rhs_val = numbers[rhs]
    res = 0
    if op == "+":
        res = lhs_val + rhs_val
    elif op == "-":
        res = lhs_val - rhs_val
    elif op == "*":
        res = lhs_val * rhs_val
    elif op == "/":
        res = lhs_val // rhs_val
    return res


def main():
    numbers: Dict[str, int] = {}
    expressions: Dict[str, Tuple[str, str, str]] = {}

    parse_input("input.txt", numbers, expressions)
    # print(numbers)
    # print(expressions)
    while "root" in expressions:
        next_expr = ""
        for key, val in expressions.items():
            if val[0] in numbers and val[2] in numbers:
                next_expr = key
                break
        numbers[next_expr] = calc_expr(expressions[next_expr], numbers)
        expressions.pop(next_expr)
    assert "root" in numbers
    print(numbers["root"])


if __name__ == "__main__":
    main()
