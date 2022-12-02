def main():
    with open("input.txt", "r") as f:
        calories_per_elf = []
        accumulated_calories = 0
        for line in f:
            if len(line.strip()) == 0:
                calories_per_elf.append(accumulated_calories)
                accumulated_calories = 0
            else:
                accumulated_calories += int(line)
        calories_per_elf.append(accumulated_calories)
        calories_per_elf.sort(reverse=True)
        assert(len(calories_per_elf) >= 3)
        top3_calory_sum = calories_per_elf[0] + calories_per_elf[1] + calories_per_elf[2]
        print(top3_calory_sum)

if __name__ == "__main__":
    main()
