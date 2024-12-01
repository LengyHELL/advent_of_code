"""
Advent of Code Day 23
"""

import sys
from functools import lru_cache
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

    def __sub__(self, other: "Coord"):
        return Coord(self.x - other.x, self.y - other.y)

    def __eq__(self, other: "Coord"):
        return self.x == other.x and self.y == other.y

    def __mul__(self, number: int):
        return Coord(self.x * number, self.y * number)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

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
    previous: "Node"

    def __init__(
        self, position: Coord, weight: int = 0, previous: "Node" = None
    ) -> None:
        self.position = position
        self.weight = weight
        self.previous = previous

    def __eq__(self, other: "Node"):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __str__(self):
        return f"<node {self.position}>"

    def __repr__(self):
        return self.__str__()


class Trails:
    trails_map: list[str]
    width: int
    height: int
    start: Coord
    end: Coord
    path: list[Coord]
    junctions: list[Node]
    longest_path: int
    paths: int

    def __init__(
        self,
        trails_map: list[str],
    ):
        self.trails_map = trails_map.copy()
        self.width = len(trails_map)
        self.height = len(trails_map[0])
        self.start = Coord(trails_map[0].find("."), 0)
        self.end = Coord(trails_map[-1].find("."), self.height - 1)
        self.path = []
        self.junctions = []
        self.longest_path = 0
        self.paths = 0

    def __str__(self):
        drawing = ""

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if position == self.start:
                    drawing += colored(value, "white", "on_blue")
                elif position == self.end:
                    drawing += colored(value, "white", "on_red")
                elif position in self.path:
                    drawing += colored(value, "white", "on_green")
                else:
                    drawing += value

            if y < self.height - 1:
                drawing += "\n"

        return drawing

    def __repr__(self):
        return f"<trails_map [{self.width} x {self.height}]>"

    def get(self, point: Coord):
        x, y = point
        return self.trails_map[y][x]

    def find_path(self):
        self.path.clear()
        queue: list[Node] = [Node(self.start)]
        checked = set[Node]()
        directions = [
            (Coord(0, -1), ".^"),
            (Coord(0, 1), ".v"),
            (Coord(1, 0), ".>"),
            (Coord(-1, 0), ".<"),
        ]

        while len(queue) > 0:
            current = queue.pop(0)
            checked.add(current)

            if current.position == self.end:
                path = []
                temp = current

                while temp is not None:
                    path.insert(0, temp.position)
                    temp = temp.previous

                if len(path) > len(self.path):
                    self.path = path

                continue

            for direction, possible in directions:
                new_node = Node(
                    current.position + direction, current.weight + 1, current
                )

                if self.get(new_node.position) not in possible:
                    continue

                if (
                    current.previous is not None
                    and new_node.position == current.previous.position
                ):
                    continue

                queue.append(new_node)

    @lru_cache
    def junction_distance(self, start: Node, end: Node):
        queue: list[Node] = [Node(start.position)]
        directions = [
            Coord(0, -1),
            Coord(0, 1),
            Coord(1, 0),
            Coord(-1, 0),
        ]

        other_junctions = self.junctions.copy()

        if start in other_junctions:
            other_junctions.remove(start)

        if end in other_junctions:
            other_junctions.remove(end)

        for current in queue:
            if current == end:
                return current.weight

            for direction in directions:
                new_position = current.position + direction
                new_node = Node(new_position, current.weight + 1, current)

                if (
                    new_position.x < 0
                    or new_position.y < 0
                    or new_position.x >= self.width
                    or new_position.y >= self.height
                ):
                    continue

                if (
                    self.get(new_position) != "#"
                    and new_node not in queue
                    and new_node not in other_junctions
                ):
                    queue.append(new_node)

        return None

    def get_route(self, start: Node, end: Node, junctions: list[Node]):
        new_junctions = junctions.copy()
        new_junctions.remove(start)
        highest = 0

        for junction in new_junctions:
            distance = self.junction_distance(start, junction)

            if distance is not None:
                junction.previous = start
                junction.weight = start.weight + distance
                if junction == end:
                    highest = max(highest, junction.weight)
                    self.paths += 1
                    end = "\r"
                    if highest > self.longest_path:
                        self.longest_path = highest
                        end = "\n"
                    print(
                        f"Current longest path is {self.longest_path} of {self.paths} paths",
                        end=end,
                    )
                else:
                    highest = max(highest, self.get_route(junction, end, new_junctions))

        return highest

    def find_longest_path(self):
        self.junctions = []
        self.longest_path = 0
        self.paths = 0
        directions = [
            Coord(0, -1),
            Coord(0, 1),
            Coord(1, 0),
            Coord(-1, 0),
        ]

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.get(Coord(x, y)) == "#":
                    continue

                roads = 0

                for direction in directions:
                    if self.get(Coord(x, y) + direction) != "#":
                        roads += 1
                if roads > 2:
                    self.junctions.append(Node(Coord(x, y)))

        self.junctions.append(Node(self.start))
        self.junctions.append(Node(self.end))

        self.get_route(Node(self.start), Node(self.end), self.junctions)


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        trails = Trails(file.read().splitlines())

        trails.find_path()
        # print(trails)
        print(f"The longest hike's length is {len(trails.path) - 1}")

        trails.find_longest_path()
        print(
            f"The longest hike's length when the trails are not slippery is {trails.longest_path}"
        )


if __name__ == "__main__":
    main()

# 4926 too low
# 6003 too low
# 6074 too low ?
# 9472 too high (max)
