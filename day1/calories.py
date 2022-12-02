def main():
    with open("input.txt", "r") as f:
        max_calories = 0
        accumulated_calories = 0
        for line in f:
            if len(line.strip()) == 0:
                max_calories = max(max_calories, accumulated_calories)
                accumulated_calories = 0
            else:
                accumulated_calories += int(line)
        max_calories = max(max_calories, accumulated_calories)
        print(max_calories)

if __name__ == "__main__":
    main()
