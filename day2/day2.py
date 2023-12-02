"""
Advent of Code Day 2
"""

import re
import sys

with open(sys.argv[1], encoding="utf-8") as file:
    lines = file.read().split("\n")
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    sum_of_ids = 0
    sum_of_set_values = 0
    put_back = True

    for line in lines:
        game_id, game_results = re.search(r"Game (\d+): ([\d A-z,;]+)", line).groups()
        cubes = re.findall(r"(\d+ [A-z]+)", game_results)
        possible = True

        max_values = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for cube in cubes:
            value, color = cube.split(" ")
            if put_back:
                max_values[color] = max(max_values[color], int(value))
            else:
                max_values[color] += int(value)

        set_value = 1
        for color, value in max_values.items():
            if value > limits[color]:
                possible = False
            set_value *= value

        if possible:
            sum_of_ids += int(game_id)

        sum_of_set_values += set_value

    print("The sum of ids is:", sum_of_ids)
    print("The sum of the set values is:", sum_of_set_values)
