"""
Advent of Code 2025 Day 1
"""

import sys
import re


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().split("\n")
        dial_pos = 50
        zeros = 0

        for line in lines:
            match = re.match(r"([LR])([0-9]+)", line)
            direction, amount = match.groups()

            if direction == "R":
                dial_pos += int(amount)
            elif direction == "L":
                dial_pos -= int(amount)

            while dial_pos < 0:
                dial_pos += 100

            while dial_pos > 99:
                dial_pos -= 100

            if dial_pos == 0:
                zeros += 1

        print(f"The password for part 1 is {zeros}.")

        dial_pos = 50
        zeros = 0

        for line in lines:
            match = re.match(r"([LR])([0-9]+)", line)
            direction, amount = match.groups()

            offset = int(amount)
            modifier = 1 if direction == "R" else -1

            for _ in range(offset):
                dial_pos += modifier

                if dial_pos < 0:
                    dial_pos += 100
                elif dial_pos > 99:
                    dial_pos -= 100

                if dial_pos == 0:
                    zeros += 1

        print(f"The password for part 2 is {zeros}.")
        # 5795 too low


if __name__ == "__main__":
    main()
