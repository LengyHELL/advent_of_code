"""
Advent of Code Day 17
"""

import sys
from queue import PriorityQueue

from termcolor import colored


class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other: "Coord"):
        return Coord(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Coord"):
        return self.x == other.x and self.y == other.y

    def __mul__(self, number: int):
        return Coord(self.x * number, self.y * number)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y)

    def distance(self, other: "Coord"):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def rotate(self, clockwise=True):
        x, y = self.y, self.x
        if clockwise:
            x *= -1
        else:
            y *= -1
        return Coord(x, y)


class Node:
    position: Coord
    weight: int
    horizontal: bool
    previous: "Node"

    def __init__(
        self,
        position: Coord,
        weight: int,
        horizontal: bool,
        previous: "Node" = None,
    ):
        self.position = position
        self.weight = weight
        self.horizontal = horizontal
        self.previous = previous

    def __eq__(self, other: "Node"):
        return self.position == other.position and self.horizontal == other.horizontal

    def __lt__(self, other: "Node"):
        return (
            self.weight,
            (
                self.position.x,
                self.position.y,
                self.horizontal,
            ),
        ) < (
            other.weight,
            (
                other.position.x,
                other.position.y,
                other.horizontal,
            ),
        )

    def __hash__(self):
        return hash((self.position.x, self.position.y, self.horizontal))

    def __repr__(self):
        return f"{self.position} - {self.weight}"

    def copy(self):
        return Node(self.position, self.weight, self.horizontal, self.previous)


class HeatMap:
    heat_map: list[list[float]]
    width: int
    height: int
    route: list[Coord] = []
    minimum_heat_loss: int = float("inf")

    def __init__(
        self,
        heat_map: list[list[float]],
    ):
        self.heat_map = heat_map.copy()
        self.width = len(heat_map)
        self.height = len(heat_map[0])

    def __str__(self):
        drawing = ""
        fill = self.get_fill(self.heat_map)

        for y, line in enumerate(self.heat_map):
            for x, value in enumerate(line):
                current: str = ""

                if value == float("inf"):
                    current = f"{'-':{fill}}"
                else:
                    current = f"{value:<{fill}.0f}"

                if Coord(x, y) in self.route:
                    drawing += colored(current, "white", "on_green")
                else:
                    drawing += current

            if y < (self.height - 1):
                drawing += "\n"

        return drawing

    def get_fill(self, float_map: list[list[float]]):
        flattened: list[float] = []

        for line in float_map:
            flattened.extend(line)

        flattened = [item for item in flattened if item != float("inf")]

        return len(f"{max(flattened):.0f}")

    def get(self, point: Coord):
        return self.heat_map[point.y][point.x]

    def set(self, point: Coord, value: float):
        self.heat_map[point.y][point.x] = value

    def calculate_weights(
        self,
        min_straight=1,
        max_straight=3,
        start: Coord = None,
        end: Coord = None,
    ):
        start = Coord(0, 0) if start is None else start
        end = Coord(self.width - 1, self.height - 1) if end is None else end

        queue = PriorityQueue[Node]()
        queue.put(Node(start, 0, True))
        queue.put(Node(start, 0, False))
        checked = set[Node]()

        while queue:
            current = queue.get()

            if current.position == end:
                self.minimum_heat_loss = current.weight
                self.route = []
                while current is not None:
                    self.route.insert(0, current.position)
                    current = current.previous
                break
            if current in checked:
                continue

            checked.add(current)

            for side in [-1, 1]:
                previous_node = current

                for straight in range(1, max_straight + 1):
                    position: Coord
                    if current.horizontal:
                        position = current.position + Coord(side, 0) * straight
                    else:
                        position = current.position + Coord(0, side) * straight

                    if (
                        position.x < 0
                        or position.x >= self.width
                        or position.y < 0
                        or position.y >= self.height
                    ):
                        break

                    weight = previous_node.weight + self.get(position)
                    new_node = Node(
                        position, weight, not current.horizontal, previous_node
                    )
                    previous_node = new_node

                    if new_node in checked:
                        continue
                    if straight >= min_straight:
                        queue.put(new_node)


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().split("\n")
        for index, line in enumerate(lines):
            lines[index] = [float(value) for value in line]

        heat_map = HeatMap(lines)
        heat_map.calculate_weights()
        print(heat_map)
        print(f"The minimum heat loss is {heat_map.minimum_heat_loss:.0f}")

        heat_map.calculate_weights(4, 10)
        print(heat_map)
        print(
            f"The minimum heat loss with ultra crucibles is {heat_map.minimum_heat_loss:.0f}"
        )


if __name__ == "__main__":
    main()
