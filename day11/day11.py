"""
Advent of Code Day 10
"""

import sys


def get_distance(source: int, destination: int, mask: str, empty_space_multiplier: int):
    """
    Gets the one dimensional distance between two points
    """
    values = [source, destination]
    start, end = [min(values), max(values)]
    empty_space = mask[start:end].count(".")

    return (
        abs(destination - source) - empty_space
    ) + empty_space * empty_space_multiplier


with open(sys.argv[1], encoding="utf-8") as file:
    space = file.read().split("\n")
    empty_space_multiplier = 1000000
    sum_of_distances = 0
    stars: list[tuple[int, int]] = []
    v_mask = "".ljust(len(space), ".")
    h_mask = "".ljust(len(space[0]), ".")

    for index, row in enumerate(space):
        empty = True
        location = -1

        while (location := row.find("#", location + 1)) >= 0:
            empty = False
            h_mask = h_mask[:location] + "#" + h_mask[location + 1 :]
            stars.append((index, location))

        if not empty:
            v_mask = v_mask[:index] + "#" + v_mask[index + 1 :]

    for index, star in enumerate(stars):
        for compare in stars[index:]:
            v_distance = get_distance(
                star[0], compare[0], v_mask, empty_space_multiplier
            )
            h_distance = get_distance(
                star[1], compare[1], h_mask, empty_space_multiplier
            )
            sum_of_distances += v_distance + h_distance

    print("The sum of the shortest paths with")
    print(f"\tx{empty_space_multiplier}")
    print("empty space multiplier is")
    print(f"\t{sum_of_distances}")
