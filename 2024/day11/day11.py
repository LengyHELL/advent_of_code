"""
Advent of Code Day 11
"""

import sys
import re

from functools import cache


def calculate_stone(stone: str):
    if stone == "0":
        return ["1"]
    elif (chunk := len(stone)) % 2 == 0:
        chunk = int(chunk / 2)
        return [str(int(stone[i : i + chunk])) for i in range(0, len(stone), chunk)]
    else:
        return [str(int(stone) * 2024)]


@cache
def get_stones(stone: str, blink: int, blinks: int) -> int:
    if blink >= blinks:
        return 1

    total = 0
    new_stone = calculate_stone(stone)

    for ns in new_stone:
        total += get_stones(ns, blink + 1, blinks)

    return total


def get_stones_after(stones: list[str], blinks: int):
    total = 0
    for stone in stones:
        total += get_stones(stone, 0, blinks)

    return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        stones = re.findall(r"(\d+)", file.read())

        print(f"There are {get_stones_after(stones, 25)} stones after 25 blinks.")
        print(f"There are {get_stones_after(stones, 75)} stones after 75 blinks.")


if __name__ == "__main__":
    main()
