#!/usr/bin/env python3


def print_display(display):
    for line in display:
        print("".join(line))



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

    width = 40
    height = 6
    display = [["." for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sprite_middle = all_reg_values[width * y + x]
            if sprite_middle - 1 <= x <= sprite_middle + 1:
                display[y][x] = "#"
    
    print_display(display)
                


if __name__ == "__main__":
    main()
