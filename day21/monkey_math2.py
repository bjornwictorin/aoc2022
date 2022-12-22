#!/usr/bin/env python3

from typing import Dict, Tuple, Set


def parse_input(file_name: str, numbers: Dict[str, int], expressions: Set[Tuple[str, str, str, str]]) -> None:
    with open(file_name, "r") as f:
        for line in f:
            key, value = line.split(": ")
            if value.strip().isnumeric():
                numbers[key] = int(value)
            else:
                lhs, op, rhs = value.strip().split(" ")
                expressions.add((key, lhs, op, rhs))


def rewrite_expr(label: str, label_expr: Tuple[str, str, str, str]) -> Tuple[str, str, str, str]:
    # Handle special case if key == "root" (in that case the op is =)
    res, lhs, op, rhs = label_expr
    if label == res:
        return label_expr
    elif res == "root": # rhs = lhs <=> rhs = 1 * lhs <=> lhs = 1 * rhs
        return (label, "one", "*", lhs if label == rhs else rhs)
    elif op == "+":
        if label == lhs: # res = lhs + rhs <=> lhs = res - rhs
            return (lhs, res, "-", rhs)
        else:
            assert label == rhs # res = lhs + rhs <=> rhs = res - lhs
            return (rhs, res, "-", lhs)
    elif op == "-":
        if label == lhs: # res = lhs - rhs <=> lhs = res + rhs
            return (lhs, res, "+", rhs)
        else:
            assert label == rhs # res = lhs - rhs <=> rhs = lhs - res
            return (rhs, lhs, "-", res)
    elif op == "*":
        if label == lhs: # res = lhs * rhs <=> lhs = res / rhs
            return (lhs, res, "/", rhs)
        else:
            assert label == rhs # res = lhs * rhs <=> rhs = res / lhs
            return (rhs, res, "/", lhs)
    elif op == "/":
        if label == lhs: # res = lhs / rhs <=> lhs = res * rhs
            return (lhs, res, "*", rhs)
        else:
            assert label == rhs # res = lhs / rhs <=> rhs = lhs / res
            return (rhs, lhs, "/", res)
    else:
        assert False, f"Invalid op: {op}"


def do_math(lhs_val: int, op: str, rhs_val: int) -> int:
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


def calc_value(label: str, numbers: Dict[str, int], expressions: Set[Tuple[str, str, str, str]]) -> int:
    # If expression is a number, return the number
    if label in numbers:
        return numbers[label]
    # Find expression containing label
    label_expr = ("", "", "", "")
    for expr in expressions:
        if label in expr:
            label_expr = expr
            break
    # Each expression may only be used once
    expressions.remove(label_expr)
    assert label_expr != ("", "", "", ""), f"Error finding label_expr for label: {label}"
    # Rewrite expression to get var_name alone on one side of =
    res, lhs, op, rhs = rewrite_expr(label, label_expr)
    assert res == label, "Rewritten expr should calculate label"
    # Calc the operands
    lhs_val = calc_value(lhs, numbers, expressions)
    rhs_val = calc_value(rhs, numbers, expressions)
    # Do the calculation
    res = do_math(lhs_val, op, rhs_val)
    # Return result
    return res


def main():
    numbers: Dict[str, int] = {}
    expressions: Set[Tuple[str, str, str, str]] = set()
    parse_input("input.txt", numbers, expressions)
    numbers.pop("humn")
    numbers["one"] = 1 # Used for root calc
    # print(numbers)
    # print(expressions)
    res = calc_value("humn", numbers, expressions)
    print(res)


if __name__ == "__main__":
    main()
