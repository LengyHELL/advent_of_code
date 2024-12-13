"""
Advent of Code Day 13
"""

import sys
import re


def get_tokens(machines: list[tuple[int, ...]], modifier=0, round_decimals=3):
    tokens = 0
    for a_x, a_y, b_x, b_y, prize_x, prize_y in machines:
        prize_x += modifier
        prize_y += modifier

        press_a = round(
            (prize_y - (b_y * prize_x) / b_x) / (a_y - (a_x * b_y) / b_x),
            round_decimals,
        )
        press_b = round((prize_x - a_x * press_a) / b_x, round_decimals)

        if press_a.is_integer() and press_b.is_integer():
            tokens += int(press_a) * 3 + int(press_b)

    return tokens


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        machines = list(
            map(
                lambda x: tuple(map(int, x)),
                re.findall(
                    r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
                    file.read(),
                ),
            )
        )

        print(
            f"The fewest tokens to spend for all the possible prizes is {get_tokens(machines)}."
        )
        print(
            f"The fewest tokens to spend for all the possible prizes is {get_tokens(machines, 10000000000000, 2)}."
        )


if __name__ == "__main__":
    main()
