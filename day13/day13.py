"""
Advent of Code Day 13
"""

import sys


def get_diffs(lower_row: str, upper_row: str):
    diffs = 0
    size = min(len(lower_row), len(upper_row))

    for i in range(size):
        if lower_row[i] != upper_row[i]:
            diffs += 1

    return diffs


def get_reflection_point(lines: list[str], smudges=0):
    """
    Gets the bottom or right side of the reflection line
    """
    for index in range(1, len(lines)):
        if (total_diffs := get_diffs(lines[index - 1], lines[index])) <= 1:
            offset = 1
            mirror = True

            while (0 <= (lower := index - offset - 1)) and (
                (upper := index + offset) < len(lines)
            ):
                total_diffs += get_diffs(lines[lower], lines[upper])

                if lines[lower] != lines[upper] and total_diffs > smudges:
                    mirror = False
                    break

                offset += 1

            if mirror and total_diffs == smudges:
                return index

    return None


with open(sys.argv[1], encoding="utf-8") as file:
    blocks = file.read().split("\n\n")
    mirror_value = 0
    smudges = 1  # set to 0 for part 1

    for block in blocks:
        total = 0
        vertical = horizontal = None

        rows = block.split("\n")

        if (horizontal := get_reflection_point(rows, smudges)) is not None:
            mirror_value += 100 * horizontal

        columns = ["".join([row[i] for row in rows]) for i in range(len(rows[0]))]

        if (vertical := get_reflection_point(columns, smudges)) is not None:
            mirror_value += vertical

        print(f"| horizontal {str(horizontal):>15} | vertical {str(vertical):>15} |")

    print(f"The mirror value is {mirror_value}")
