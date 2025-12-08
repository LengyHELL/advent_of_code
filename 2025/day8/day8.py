"""
Advent of Code 2025 Day 8
"""

import sys
import bisect

from typing import Dict, Set, List, Tuple
from functools import cache
from math import sqrt, prod

class Box:
    x: int
    y: int
    z: int
    circuit: int

    def __init__(self, x: int, y: int, z: int, circuit: int):
        self.x = x
        self.y = y
        self.z = z
        self.circuit = circuit

    def __str__(self):
        return f"({self.x},{self.y},{self.z}) - {self.circuit}"

    def __repr__(self):
        return f"({self.x},{self.y},{self.z}) - {self.circuit}"

    def __eq__(self, other: "Box"):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.circuit == other.circuit

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.circuit))

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.circuit))

    def copy(self):
        return Box(self.x, self.y, self.z, self.circuit)

@cache
def get_box_distance(box1: Box, box2: Box) -> int:
    return sqrt((box2.x - box1.x)**2 + (box2.y - box1.y)**2 + (box2.z - box1.z)**2)

def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().splitlines()
        boxes = list(map(
            lambda b: Box(int(b[1][0]), int(b[1][1]), int(b[1][2]), b[0]),
            [(i, box.split(",")) for i, box in enumerate(lines)]
        ))
        connections = int(input("Connections: "))

        distances: List[Tuple[int, int, int]] = []

        for i in range(len(boxes) - 1):
            print(f"Distances {i + 1:<{len(str(len(boxes) - 1))}} / {len(boxes)}", end="\r")
            b1 = boxes[i]

            for b2 in boxes[i + 1:]:
                distance = get_box_distance(b1, b2)
                indexes = (i, boxes.index(b2))
                bisect.insort(distances, (*indexes, distance), key=lambda x: x[-1])

        c = 0
        extension = 0

        while True:
            if connections != 0 and c >= connections:
                break
            print(f"Connection {c + 1:<{len(str(connections))}} / {connections}", end="\r")
            if c >= len(distances):
                break

            t, f, _ = distances[c]
            old = boxes[f].circuit

            for j, b in enumerate(boxes):
                if b.circuit == old:
                    boxes[j].circuit = boxes[t].circuit

            if all([b.circuit == boxes[0].circuit for b in boxes]):
                extension = boxes[t].x * boxes[f].x
                break

            c += 1


        circuits: Dict[int, Set[Box]] = dict()
        for b in boxes:
            if b.circuit in circuits:
                circuits[b.circuit].add(b)
            else:
                circuits[b.circuit] = set([b])

        total = prod(sorted(map(len, circuits.values()), reverse=True)[:3])

        print(f"The multiple of the 3 largest after {connections if connections == 1 else 'infinite'} connections circuits is {total}.")

        if connections == 0:
            print(f"The length of the extension cable should be {extension}.")


if __name__ == "__main__":
    main()
