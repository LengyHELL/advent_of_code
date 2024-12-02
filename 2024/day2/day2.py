"""
Advent of Code Day 2
"""

import sys
import re


def check_for_safe(levels, limit=3):
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]
    asc_safes = [0 < diff <= limit for diff in diffs]
    desc_safes = [-limit <= diff < 0 for diff in diffs]

    return asc_safes.count(False) == 0 or desc_safes.count(False) == 0


with open(sys.argv[1], encoding="utf-8") as file:
    safe_reports = 0
    safe_reports_with_dampener = 0

    for line in file.read().split("\n"):
        levels = list(map(int, re.findall(r"(\d+)", line)))

        if check_for_safe(levels):
            safe_reports += 1
        else:
            filtered_levels = []
            for i in range(len(levels)):
                temp = levels.copy()
                temp.pop(i)
                filtered_levels.append(temp)

            if any(check_for_safe(filtered) for filtered in filtered_levels):
                safe_reports_with_dampener += 1

    print(f"There are {safe_reports} safe reports.")
    print(
        f"There are {safe_reports + safe_reports_with_dampener} safe reports with the dampener."
    )
