"""
Advent of Code 2025 Day 5
"""

import sys


def overlaps(x: tuple[int, int], y: tuple[int, int]) -> bool:
    x_start, x_end = x
    y_start, y_end = y

    return x_start <= y_end and y_start <= x_end


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        ranges, ingredients = file.read().split("\n\n")
        ranges = [
            (int(r.split("-")[0]), int(r.split("-")[1])) for r in ranges.split("\n")
        ]
        ingredients = [int(i) for i in ingredients.split("\n")]

        fresh = 0

        for i in ingredients:
            for s, e in ranges:
                if s <= i <= e:
                    fresh += 1
                    break

        has_overlap = True

        while has_overlap:
            has_overlap = False

            for i, x in enumerate(ranges):
                for j in range(i, len(ranges)):
                    if i == j:
                        continue

                    y = ranges[j]

                    if x == y:
                        ranges.remove(y)
                        has_overlap = True
                        break

                    if overlaps(x, y):
                        new_range = (min([*x, *y]), max([*x, *y]))
                        ranges.remove(x)
                        ranges.remove(y)
                        ranges.append(new_range)
                        has_overlap = True
                        break

                if has_overlap:
                    break

        possible = 0

        for s, e in ranges:
            possible += (e + 1) - s

        print(f"There are {fresh} fresh ingredients.")
        print(f"There could be {possible} possibly fresh ingredients.")
        # 367875991070099 too high


if __name__ == "__main__":
    main()
