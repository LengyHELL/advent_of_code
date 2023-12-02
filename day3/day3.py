"""
Advent of Code Day 3
"""

import re
import sys
from functools import reduce
import operator


def prod(iterable):
    """
    Returns the product of the given list of numbers
    """
    return reduce(operator.mul, iterable, 1)


with open(sys.argv[1], encoding="utf-8") as file:
    engine = file.read().split("\n")
    width = len(engine[0])

    sum = 0
    gears = {}

    for index, line in enumerate(engine):
        numbers = re.finditer(r"\d+", line)

        for number in numbers:
            for row in range(-1, 2):
                if 0 <= row + index < len(engine):
                    start = number.span()[0] - 1
                    end = number.span()[1] + 1

                    for column in range(start, end):
                        if 0 <= column < width:
                            if re.match(r"[^\dA-z.]", engine[row + index][column]):
                                number_start, number_end = number.span()
                                sum += int(line[number_start:number_end])

                                if engine[row + index][column] == "*":
                                    gear_id = (row + index) * width + column
                                    if gear_id in gears:
                                        gears[gear_id].append(
                                            int(line[number_start:number_end])
                                        )
                                    else:
                                        gears[gear_id] = [
                                            int(line[number_start:number_end])
                                        ]

    gear_ratios = 0
    for _, gear in gears.items():
        if len(gear) > 1:
            gear_ratios += prod(gear)

    print("The sum is:", sum)
    print("The sum of the gear ratios is:", gear_ratios)
