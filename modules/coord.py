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

    def __lt__(self, other: "Coord"):
        return self.x < other.x and self.y < other.y

    def __gt__(self, other: "Coord"):
        return self.x > other.x and self.y > other.y

    def __le__(self, other: "Coord"):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other: "Coord"):
        return self.x >= other.x and self.y >= other.y

    def __mul__(self, number: int):
        return Coord(self.x * number, self.y * number)

    __rmul__ = __mul__

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def copy(self):
        return Coord(self.x, self.y)

    def distance(self, other: "Coord" = None):
        if other is None:
            other = Coord(0, 0)
        return abs(other.x - self.x) + abs(other.y - self.y)

    def rotate(self, clockwise=True):
        x, y = self.y, self.x
        if clockwise:
            x *= -1
        else:
            y *= -1
        return Coord(x, y)

    def abs(self):
        return Coord(abs(self.x), abs(self.y))

    def det(self, other: "Coord"):
        return self.x * other.y - self.y * other.x
