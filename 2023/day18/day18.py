"""
Advent of Code Day 18
"""

import sys
import re


def add(left: tuple[int, int], right: tuple[int, int]):
    return (left[0] + right[0], left[1] + right[1])


def multiply(coord: tuple[int, int], number: int):
    return (coord[0] * number, coord[1] * number)


def calculate_perimeter(points: list[int, int]):
    perimeter = 0
    for i, point in enumerate(points):
        perimeter += abs(point[0] - points[i - 1][0]) + abs(point[1] - points[i - 1][1])
    return perimeter


def calculate_area(points: list[int, int]):
    area = 0
    for i in range(-1, len(points) - 1):
        area += points[i][0] * (points[i + 1][1] - points[i - 1][1])
    return abs(area) // 2 + calculate_perimeter(points) // 2 + 1


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = re.findall(r"([UDLR]) (\d+) \(#([\da-f]+)\)", file.read())

        directions: dict[str, tuple[int, int]] = {
            "R": (1, 0),
            "D": (0, 1),
            "L": (-1, 0),
            "U": (0, -1),
        }

        hex_directions: dict[str, tuple[int, int]] = {
            "0": (1, 0),
            "1": (0, 1),
            "2": (-1, 0),
            "3": (0, -1),
        }

        current = (0, 0)
        hex_current = (0, 0)

        corners = []
        hex_corners = []

        for direction_key, amount_string, hex_number in lines:
            direction = directions[direction_key]
            hex_direction = hex_directions[hex_number[-1]]

            amount = int(amount_string)
            hex_amount = int(hex_number[:-1], 16)

            corners.append(current)
            hex_corners.append(hex_current)

            current = add(current, multiply(direction, amount))
            hex_current = add(hex_current, multiply(hex_direction, hex_amount))

        area = calculate_area(corners)
        hex_area = calculate_area(hex_corners)

        print(f"The area of the trench is {area}")
        print(f"The area of the trench using the hex number is {hex_area}")


if __name__ == "__main__":
    main()
