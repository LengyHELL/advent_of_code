"""
Advent of Code Day 4
"""

import re
import sys


def get_number_array(string: str):
    """
    Creates a number array from a string containing a list of numbers
    """
    return [int(number) for number in string.strip().replace("  ", " ").split(" ")]


def solve_part_one(data: str):
    """
    Solves part one of the puzzle
    """
    total_points = 0

    for line in data.split("\n"):
        _, winning_string, chosen_string = re.search(
            r"Card[ ]+(\d+): ([\d ]+) \| ([\d ]+)", line
        ).groups()
        winning = get_number_array(winning_string)
        chosen = get_number_array(chosen_string)
        points = 0

        for win in winning:
            if win in chosen:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        total_points += points

        # print(winning, chosen, points)
    print("Total winning points:", total_points)


def get_cards(match_list: list[int]):
    """
    I dont know yet
    """
    scores = []

    for matches in match_list:
        score = 1

        for index in range(matches):
            score += scores[-(index + 1)]

        scores.append(score)
    return sum(scores)


def solve_part_two(data: str):
    """
    Solves part two of the puzzle
    """
    lines = data.split("\n")
    match_list = []

    for line in lines:
        _, winning_string, chosen_string = re.search(
            r"Card[ ]+(\d+): ([\d ]+) \| ([\d ]+)", line
        ).groups()
        winning = get_number_array(winning_string)
        chosen = get_number_array(chosen_string)
        matches = 0

        for win in winning:
            if win in chosen:
                matches += 1
        match_list.append(matches)

    print("Total number of cards:", get_cards(match_list[::-1]))


with open(sys.argv[1], encoding="utf-8") as file:
    file_data = file.read()
    solve_part_one(file_data)
    solve_part_two(file_data)
