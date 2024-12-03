"""
Advent of Code Day 3
"""

import sys
import re

with open(sys.argv[1], encoding="utf-8") as file:
    operations = re.findall(r"(mul|do|don't)\((?:(\d+),(\d+))?\)", file.read())
    result = 0
    instructions_enabled = True

    for operation, x, y in operations:
        if operation in {"do", "don't"}:
            instructions_enabled = operation == "do"
        elif operation == "mul" and instructions_enabled:
            result += int(x) * int(y)

    print(f"The sum of the results is {result}.")
