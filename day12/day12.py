"""
Advent of Code Day 12
"""

import sys
from functools import lru_cache


@lru_cache
def get_arrangements(row: str, groups: tuple[int, ...]):
    """
    Returns all possible arrangements for the given row
    """
    arrangements = 0

    if not groups:
        return 1 if "#" not in row else 0

    for index in range(len(row) - sum(groups) - len(groups) + 2):
        end = index + groups[0]

        if "#" in row[:index]:
            break

        if end <= len(row) and "." not in row[index:end] and row[end : end + 1] != "#":
            arrangements += get_arrangements(row[end + 1 :], groups[1:])

    return arrangements


with open(sys.argv[1], encoding="utf-8") as file:
    lines = file.read().splitlines()
    sum_of_arrangements = 0
    folds = 5
    total = len(lines)
    fill = len(str(total))

    for index, line in enumerate(lines):
        print(f"Progress: {index + 1:{fill}}/{total:{fill}}", end="\r")
        row, groups = line.split(" ")
        groups = tuple(int(number) for number in groups.split(","))

        row = "?".join([row] * folds)
        groups = groups * folds

        sum_of_arrangements += get_arrangements(row, groups)

    print(f"\nThe sum of the arrangements is {sum_of_arrangements}")
