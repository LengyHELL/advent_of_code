"""
Advent of Code Day 8
"""

import re
import sys
import math


def solve_part_one(directions: str, nodes: dict):
    steps = 0
    current_node = "AAA"
    while current_node != "ZZZ":
        for step in directions:
            current_node = nodes[current_node][int(step)]
            steps += 1
    return steps


def solve_part_two(directions: str, nodes: dict):
    current_nodes = [node for node in nodes.keys() if node[-1] == "A"]
    current_steps = []

    for current_node in current_nodes:
        steps = 0

        while current_node[-1] != "Z":
            for step in directions:
                current_node = nodes[current_node][int(step)]
                steps += 1

        current_steps.append(steps)

    return math.lcm(*current_steps)


with open(sys.argv[1], encoding="utf-8") as file:
    directions, nodes_raw = re.search(
        r"([RL]+)\n\n([A-Z = (,)\n]+)", file.read()
    ).groups()

    directions = directions.replace("L", "0")
    directions = directions.replace("R", "1")

    nodes = {}
    for line in nodes_raw.split("\n"):
        name, left, right = re.search(
            r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)", line
        ).groups()
        nodes[name] = (left, right)

    print(f"Took {solve_part_one(directions, nodes)} steps to reach ZZZ.")
    print(
        f"Took {solve_part_two(directions, nodes)} steps to reach every --Z node from every --A node simultaneously."
    )
