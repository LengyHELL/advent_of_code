"""
Advent of Code Day 15
"""

import sys


def hash_instruction(instruction: str):
    value = 0

    for char in instruction:
        value += ord(char)
        value *= 17
        value %= 256

    return value


with open(sys.argv[1], encoding="utf-8") as file:
    instructions = file.read().split(",")

    sum_of_results = 0
    boxes: dict[int, dict[str, int]] = {}
    for instruction in instructions:
        hash_value = hash_instruction(instruction)
        sum_of_results += hash_value

        label, value = instruction.replace("-", "=").split("=")
        box = hash_instruction(label)
        if value:
            if box not in boxes:
                boxes[box] = {}

            boxes[box][label] = int(value)
        else:
            if box in boxes:
                if label in boxes[box]:
                    boxes[box].pop(label)

                if len(boxes[box]) <= 0:
                    boxes.pop(box)

    focusing_power = 0
    for box, values in boxes.items():
        for index, (label, value) in enumerate(values.items()):
            focusing_power += (box + 1) * (index + 1) * value

    print(f"The sum of the results is {sum_of_results}")
    print(f"The focusing power of the lenses is {focusing_power}")
