"""
Advent of Code Day 12
"""

import sys
from typing import List, Dict, Set

from modules.coord import Coord
from modules.grid import Grid


class FarmField(Grid):
    areas: Dict[str, List[Coord]]
    area_sizes: Dict[str, int]
    area_perimeters: Dict[str, List[Coord]]
    area_sides: Dict[str, int]

    def __init__(
        self,
        grid: List[str],
    ):
        Grid.__init__(self, grid)

        self.areas = dict()
        self.area_sizes = dict()
        self.area_perimeters = dict()
        self.area_sides = dict()

    def __get_sides(self, area: str):
        sides = 0
        positions = self.areas[area]
        min_corner = positions[0].copy()
        max_corner = positions[0].copy()

        for position in positions:
            if position.x < min_corner.x:
                min_corner.x = position.x
            if position.x > max_corner.x:
                max_corner.x = position.x
            if position.y < min_corner.y:
                min_corner.y = position.y
            if position.y > max_corner.y:
                max_corner.y = position.y

        previous: List[Coord] = []
        for i in range(min_corner.x, max_corner.x + 1):
            filtered = sorted(
                list(filter(lambda coord: coord.x == i, positions)),
                key=lambda coord: coord.y,
            )
            diff = list(
                filter(
                    lambda coord: all(item.y != coord.y for item in previous), filtered
                )
            )

            group_list = [Coord(i, j) for j in range(filtered[0].y, filtered[-1].y + 1)]
            group = False
            groups = 0
            for item in group_list:
                if item in diff:
                    if not group:
                        groups += 1
                    group = True
                elif group:
                    group = False

            if len(diff) > 0:
                sides += groups

            previous = filtered

        previous: List[Coord] = []
        for i in range(max_corner.x, min_corner.x - 1, -1):
            filtered = sorted(
                list(filter(lambda coord: coord.x == i, positions)),
                key=lambda coord: coord.y,
            )
            diff = list(
                filter(
                    lambda coord: all(item.y != coord.y for item in previous), filtered
                )
            )

            group_list = [Coord(i, j) for j in range(filtered[0].y, filtered[-1].y + 1)]
            group = False
            groups = 0
            for item in group_list:
                if item in diff:
                    if not group:
                        groups += 1
                    group = True
                elif group:
                    group = False

            if len(diff) > 0:
                sides += groups

            previous = filtered

        previous: List[Coord] = []
        for i in range(min_corner.y, max_corner.y + 1):
            filtered = sorted(
                list(filter(lambda coord: coord.y == i, positions)),
                key=lambda coord: coord.x,
            )
            diff = list(
                filter(
                    lambda coord: all(item.x != coord.x for item in previous), filtered
                )
            )

            group_list = [Coord(j, i) for j in range(filtered[0].x, filtered[-1].x + 1)]
            group = False
            groups = 0
            for item in group_list:
                if item in diff:
                    if not group:
                        groups += 1
                    group = True
                elif group:
                    group = False

            if len(diff) > 0:
                sides += groups

            previous = filtered

        previous: List[Coord] = []
        for i in range(max_corner.y, min_corner.y - 1, -1):
            filtered = sorted(
                list(filter(lambda coord: coord.y == i, positions)),
                key=lambda coord: coord.x,
            )
            diff = list(
                filter(
                    lambda coord: all(item.x != coord.x for item in previous), filtered
                )
            )

            group_list = [Coord(j, i) for j in range(filtered[0].x, filtered[-1].x + 1)]
            group = False
            groups = 0
            for item in group_list:
                if item in diff:
                    if not group:
                        groups += 1
                    group = True
                elif group:
                    group = False

            if len(diff) > 0:
                sides += groups

            previous = filtered

        return sides

    def find_areas(self):
        checked: Set[Coord] = set()
        directions = [
            Coord(1, 0),
            Coord(0, 1),
            Coord(-1, 0),
            Coord(0, -1),
        ]

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                queue = [position]

                if position in checked:
                    continue

                true_value = self.get(position)
                index = 2
                while true_value in self.areas:
                    true_value = self.get(position) + str(index)
                    index += 1

                while len(queue) > 0:
                    current = queue.pop(0)
                    value = self.get(current)

                    if true_value not in self.areas:
                        self.areas[true_value] = [current]
                    else:
                        self.areas[true_value].append(current)

                    checked.add(current)

                    for direction in directions:
                        new_position = current + direction
                        new_value = self.get(new_position)

                        if not self.in_bounds(new_position) or new_value != value:
                            if true_value not in self.area_perimeters:
                                self.area_perimeters[true_value] = [current]
                            else:
                                self.area_perimeters[true_value].append(current)
                        elif new_position not in checked and new_position not in queue:
                            queue.append(new_position)

        for area, points in self.areas.items():
            self.area_sizes[area] = len(points)
            self.area_sides[area] = self.__get_sides(area)

    def get_fencing_price(self):
        total = 0
        for area in self.areas:
            total += self.area_sizes[area] * len(self.area_perimeters[area])
        return total

    def get_bulk_fencing_price(self):
        total = 0
        for area in self.areas:
            total += self.area_sizes[area] * self.area_sides[area]
        return total


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        field = FarmField(file.read().splitlines())

        field.print()
        field.find_areas()

        print(f"The total price of fencing all regions is {field.get_fencing_price()}.")
        print(
            f"The total price of fencing all regions with bulk discount is {field.get_bulk_fencing_price()}."
        )


if __name__ == "__main__":
    main()
