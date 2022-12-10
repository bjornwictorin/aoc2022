#!/usr/bin/env python3

def main():
    reg_value = 1
    all_reg_values = []
    with open("input.txt", "r") as f:
        for line in f:
            if line.startswith("noop"):
                all_reg_values.append(reg_value)
            elif line.startswith("addx"):
                val = int(line.split()[1])
                all_reg_values.append(reg_value)
                all_reg_values.append(reg_value)
                reg_value += int(val)
    print(all_reg_values)
    print(reg_value)

    signal_strength_sum = 0
    print(len(all_reg_values))
    for cycle in range(20, 221, 40):
        signal_strength_sum += cycle * all_reg_values[cycle-1]
    print(signal_strength_sum)
                


if __name__ == "__main__":
    main()
