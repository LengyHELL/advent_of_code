"""
Advent of Code Day 25
"""

import sys


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        keys: list[list[int]] = []
        locks: list[list[int]] = []

        for schematic in file.read().split("\n\n"):
            rows = schematic.splitlines()

            base = rows[1:-1]
            current = [0] * len(base[0])

            for b in base:
                for i in range(len(base[0])):
                    if b[i] == "#":
                        current[i] += 1

            if rows[0].startswith("#"):
                locks.append(current)
            else:
                keys.append(current)

        fit = 0

        for lock in locks:
            for key in keys:
                fits = True

                for i, l in enumerate(lock):
                    if l + key[i] > 5:
                        fits = False
                        break

                if fits:
                    fit += 1

        print(f"There are {fit} unique lock/key pairs that fit together.")


if __name__ == "__main__":
    main()
