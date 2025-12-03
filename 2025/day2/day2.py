"""
Advent of Code 2025 Day 2
"""

import sys
import re


def check_id(id: str, max: int = None) -> bool:
    length = len(id)
    check_range = max if max else length

    for i in range(2, check_range + 1):
        if length % i != 0:
            continue

        expected = id[: int(length / i)] * i

        if id == expected:
            return True

    return False


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        ranges = file.read().split(",")
        id_sum = 0
        id_sum_extended = 0

        for id_range in ranges:
            start, end = re.match(r"([0-9]+)-([0-9]+)", id_range).groups()

            for i in range(int(start), int(end) + 1):
                if check_id(str(i), 2):
                    id_sum += i
                if check_id(str(i)):
                    id_sum_extended += i

        print(f"The sum of incorrect ids is {id_sum}.")
        print(f"The sum of incorrect ids for part 2 is {id_sum_extended}.")


if __name__ == "__main__":
    main()
