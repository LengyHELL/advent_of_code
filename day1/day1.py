"""
Advent of Code Day 2
"""

import re
import sys


def convert_to_number(digit_string: str):
    """
    Converts written and string digits to integers
    """
    translate_dict = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    if digit_string in translate_dict:
        return translate_dict[digit_string]
    else:
        return digit_string


with open(sys.argv[1], encoding="utf-8") as file:
    lines = file.read().split("\n")
    calibration_number = 0

    for index, line in enumerate(lines):
        first_digit = re.search(
            r"(\d|one|two|three|four|five|six|seven|eight|nine)", line
        ).group()

        last_digit = re.search(
            r"(\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)", line[::-1]
        ).group()

        number_string = convert_to_number(first_digit) + convert_to_number(
            last_digit[::-1]
        )

        calibration_number += int(number_string)
        # print(index + 1, [first_digit, last_digit[::-1]])

    print("Calibration number:", calibration_number)
