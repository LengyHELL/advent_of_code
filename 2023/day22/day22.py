"""
Advent of Code Day 22
"""

import sys


class Coord:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other: "Coord"):
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Coord"):
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: "Coord"):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, number: int):
        return Coord(self.x * number, self.y * number, self.z * number)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y, self.z)

    def distance(self, other: "Coord"):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)


class Brick:
    """
    Represents a brick with its marginal coordinates

    ### Attributes
    `start: Coord`
        starting position of the brick, should always have lower values than `end`
    `end: Coord`
        end position of the brick
    """

    start: Coord
    end: Coord
    over: set["Brick"]
    under: set["Brick"]

    def __init__(self, start: Coord = Coord(0, 0, 0), end: Coord = Coord(0, 0, 0)):
        self.start = start.copy()
        self.end = end.copy()
        self.over = set[Brick]()
        self.under = set[Brick]()

    def __str__(self):
        return f"<brick {self.start} {self.end}>"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Brick"):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((*self.start, *self.end))

    def copy(self):
        return Brick(self.start, self.end)

    def move(self, offset: Coord):
        self.start += offset
        self.end += offset

    def collides(self, other: "Brick"):
        attributes = "xyz"
        overlap = True

        for attribute in attributes:
            range1: tuple[int, int] = (
                getattr(self.start, attribute),
                getattr(self.end, attribute),
            )
            range2: tuple[int, int] = (
                getattr(other.start, attribute),
                getattr(other.end, attribute),
            )

            if not self.overlaps(range1, range2):
                overlap = False
                break

        return overlap

    @staticmethod
    def from_data(data: str):
        start_string, end_string = data.split("~")
        start = Coord(*map(int, start_string.split(",")))
        end = Coord(*map(int, end_string.split(",")))
        return Brick(start, end)

    @staticmethod
    def overlaps(range1: tuple[int, int], range2: tuple[int, int]):
        return range1[0] <= range2[1] and range2[0] <= range1[1]


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().splitlines()
        bricks = [Brick.from_data(line) for line in lines]
        bricks.sort(key=lambda brick: (brick.start.z, brick.start.x, brick.start.y))

        settled_bricks = set[Brick]()
        max_brick = 0

        for brick in bricks:
            while brick.start.z > 1:
                temp = brick.copy()
                amount = min(-1, max_brick - temp.start.z + 1)
                temp.move(Coord(0, 0, amount))
                settle = False

                for settled in settled_bricks:
                    if temp.collides(settled):
                        settle = True
                        settled.over.add(brick)
                        brick.under.add(settled)

                if settle:
                    break
                else:
                    brick.move(Coord(0, 0, amount))

            settled_bricks.add(brick)
            max_brick = max(max_brick, brick.end.z)

        safe_bricks: list[Brick] = []

        for brick in bricks:
            if len(brick.over) <= 0:
                safe_bricks.append(brick)
                continue

            if all([len(above.under) >= 2 for above in brick.over]):
                safe_bricks.append(brick)

        print(f"There are {len(safe_bricks)} safely removeable bricks")

        total_fallen = 0
        fill = len(str(len(bricks)))

        for index, brick in enumerate(bricks):
            print(f"Checking brick {index:{fill}}/{len(bricks):{fill}}", end="\r")
            queue = [brick]
            fallen = set[Brick]()

            for current in queue:
                for over in current.over:
                    if len(over.under) > 1:
                        other = over.under.copy()
                        other.remove(current)

                        if any([support not in queue for support in other]):
                            continue

                    fallen.add(over)
                    queue.append(over)

            total_fallen += len(fallen)

        print(f"There are {total_fallen} bricks that would fall")


if __name__ == "__main__":
    main()

# 38062 too low
# 1217542 too high
