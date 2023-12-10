"""
Advent of Code Day 9
"""

import sys

with open(sys.argv[1], encoding="utf-8") as file:
    lines = file.read().split("\n")

    previous_total = 0
    next_total = 0
    for line in lines:
        serials = [[int(number) for number in line.split(" ")]]

        while any(number != 0 for number in serials[-1]):
            serials.append(
                [
                    serials[-1][index] - serials[-1][index - 1]
                    for index in range(1, len(serials[-1]))
                ]
            )

        previous_number = 0
        next_number = 0
        for serial in serials[::-1]:
            previous_number = serial[0] - previous_number
            next_number = serial[-1] + next_number

        previous_total += previous_number
        next_total += next_number

    print("The sum of the extrapolated numbers for part 1 is:", next_total)
    print("The sum of the extrapolated numbers for part 2 is:", previous_total)
