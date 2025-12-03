"""
Advent of Code 2025 Day 3
"""

import sys

from functools import cache


@cache
def get_joltage(batteries: str, size: int, index: int = 0, joltage_string="") -> str:
    battery_list = [(i, int(b)) for i, b in enumerate(list(batteries[index:]))]
    ordered = sorted(battery_list, key=lambda x: x[1], reverse=True)

    for i, item in ordered:

        if len(joltage_string) == size - 1:
            return joltage_string + str(item)

        new_joltage = get_joltage(
            batteries,
            size,
            index + i + 1,
            joltage_string + str(item),
        )

        if new_joltage == "":
            continue
        else:
            return new_joltage

    return ""


def calculate_power(banks: list[str], size: int) -> None:
    total = 0

    for batteries in banks:
        joltage = get_joltage(batteries, size)
        total += int(joltage)

    print(f"The total output joltage for size {size} is {total}.")


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        banks = file.read().split("\n")
        calculate_power(banks, 2)
        calculate_power(banks, 12)


if __name__ == "__main__":
    main()
