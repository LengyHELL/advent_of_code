"""
Advent of Code Day 7
"""

import sys


def calculate_equation(current: int, test: int, numbers: list[int]):
    total = 0

    if len(numbers) == 0:
        return 1 if current == test else 0

    next_numbers = numbers.copy()
    next_number = next_numbers.pop(0)

    for i in range(3):
        if i == 0:
            total += calculate_equation(current + next_number, test, next_numbers)
        elif i == 1:
            total += calculate_equation(current * next_number, test, next_numbers)
        elif i == 2:
            total += calculate_equation(
                int(str(current) + str(next_number)), test, next_numbers
            )

    return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        total_calibration_result = 0

        for line in file.read().splitlines():
            values = line.split(": ")
            test = int(values[0])
            numbers = list(map(int, values[1].split(" ")))

            if calculate_equation(numbers[0], test, numbers[1:]):
                total_calibration_result += test

        print(f"The total calibration result is {total_calibration_result}.")


if __name__ == "__main__":
    main()
