"""
Advent of Code Day 6
"""

import re
import sys


def solve_part_one(races: list[list[int]]):
    """
    Solves part one of the puzzle
    """
    margin_of_error = 0

    for time, distance in races:
        possible = 0

        for push in range(1, time):
            if (time - push) * push > distance:
                possible += 1

        if margin_of_error == 0:
            margin_of_error = possible
        else:
            margin_of_error *= possible

    return margin_of_error


def solve_part_two(time: int, distance: int):
    """
    Solves part two of the puzzle
    """
    possible = 0
    for push in range(1, time):
        if (time - push) * push > distance:
            possible += 1
    return possible


with open(sys.argv[1], encoding="utf-8") as file:
    times, distances = re.search(
        r"Time: +([\d ]+)\nDistance: +([\d ]+)", file.read()
    ).groups()

    combined_time = int(re.sub(r" +", "", times))
    combinded_distance = int(re.sub(r" +", "", distances))

    times = re.sub(r" +", " ", times).split(" ")
    distances = re.sub(r" +", " ", distances).split(" ")

    races = [[int(times[index]), int(distances[index])] for index in range(len(times))]

    print("The margin of error for part 1 is:", solve_part_one(races))
    print(
        "The margin of error for part 2 is:",
        solve_part_two(combined_time, combinded_distance),
    )
