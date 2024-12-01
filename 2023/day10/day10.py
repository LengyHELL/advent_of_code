"""
Advent of Code Day 10
"""

import sys
from termcolor import colored


class Node:
    """
    Node class for managing pipe nodes
    """

    position: tuple[int, int]
    parent = None
    depth: int

    def __init__(self, position: tuple[int, int], parent, depth: int):
        self.position = position
        self.depth = depth
        self.parent = parent


def is_inside(polygon: list[tuple[int, int]], test: tuple[int, int]):
    """
    Checks if the given `test` point is inside the `polygon`
    """
    counter = 0

    p1y, p1x = polygon[0]
    ty, tx = test

    for index in range(1, len(polygon) + 1):
        p2y, p2x = polygon[index % len(polygon)]

        if ty > min(p1y, p2y):
            if ty <= max(p1y, p2y):
                if tx <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (ty - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                        if p1x == p2x or tx <= xinters:
                            counter += 1

        p1x = p2x
        p1y = p2y

    return counter % 2 != 0


with open(sys.argv[1], encoding="utf-8") as file:
    grid = file.read().split("\n")
    width = len(grid[0])
    height = len(grid)

    start = (0, 0)

    for row, line in enumerate(grid):
        column = line.find("S")
        if column >= 0:
            start = (row, column)

    queue = [Node(start, None, 0)]
    directions: dict[str, tuple[int, int]] = {
        "7|F": (-1, 0),
        "J-7": (0, 1),
        "L|J": (1, 0),
        "F-L": (0, -1),
    }

    index = 0
    max_depth = 0
    deepest = queue[index]
    visited = set()
    end_nodes: list[Node] = []

    while index < len(queue):
        end_nodes = []
        current_node = queue[index]

        if current_node.depth > max_depth:
            max_depth = current_node.depth
            deepest = current_node.position

        for pipes, direction in directions.items():
            check_position = (
                current_node.position[0] + direction[0],
                current_node.position[1] + direction[1],
            )

            if not (
                (0 <= check_position[0] < height) and (0 <= check_position[1] < width)
            ):
                continue

            pipe = grid[check_position[0]][check_position[1]]

            if (check_position not in visited) and (pipe in pipes):
                queue.append(Node(check_position, current_node, queue[index].depth + 1))
            elif (deepest == current_node.position) and (pipe in pipes):
                end_nodes.extend(
                    [node for node in queue if node.position == check_position]
                )

        visited.add(current_node.position)
        index += 1

    routes = []
    main_route = set([start, deepest])
    corners = [start]
    end_nodes = [end_nodes[0], Node(deepest, None, max_depth), end_nodes[1]]

    for index, node in enumerate(end_nodes):
        route = []
        while node.parent is not None:
            if grid[node.position[0]][node.position[1]] not in "|-":
                route.append(node.position)

            main_route.add(node.position)
            node = node.parent

        if index == 0:
            corners.extend(route[::-1])
        else:
            corners.extend(route)

    inside_nodes = set()

    for row, line in enumerate(grid):
        for column, node in enumerate(line):
            if ((row, column) not in main_route) and is_inside(corners, (row, column)):
                inside_nodes.add((row, column))

    for row, line in enumerate(grid):
        for column, char in enumerate(line):
            if (row, column) in corners:
                print(colored(char, "blue"), end="")
            elif (row, column) == deepest:
                print(colored(char, "red"), end="")
            elif (row, column) in inside_nodes:
                print(colored(char, "blue", "on_light_red"), end="")
            elif (row, column) in main_route:
                print(colored(char, "green"), end="")
            else:
                print(char, end="")
        print()

    print("The farthest point of the loop is:", max_depth)
    print(f"There are {len(inside_nodes)} nodes inside.")
