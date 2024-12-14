"""
Advent of Code Day 14
"""

import sys
import os
import re
from functools import reduce
from typing import List

import numpy as np
from PIL import Image

from modules.coord import Coord
from modules.grid import Grid


class Robot:
    position: Coord
    velocity: Coord

    def __init__(
        self,
        position: Coord,
        velocity: Coord,
    ):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f"<robot {self.position}>"


class BathroomMap(Grid):
    robots: List[Robot]
    simulated: int

    def __init__(
        self,
        grid: List[str],
        robot_data: str,
    ):
        Grid.__init__(self, grid)
        self.__read_robots(robot_data)
        self.simulated = 0

    def __str__(self):
        drawing = ""
        robot_positions = [robot.position for robot in self.robots]

        for y in range(self.height):
            for x in range(self.width):
                position = Coord(x, y)
                value = self.get(position)

                if (robot_count := robot_positions.count(position)) > 0:
                    drawing += str(robot_count) if robot_count < 10 else "X"
                else:
                    drawing += value

            if y < self.height:
                drawing += "\n"

        return drawing

    def __read_robots(self, data: str):
        self.robots = []

        for p_x, p_y, v_x, v_y in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", data):
            self.robots.append(
                Robot(Coord(int(p_x), int(p_y)), Coord(int(v_x), int(v_y)))
            )

    def simulate(self, seconds: int):
        for robot in self.robots:
            robot.position = self.constrain(robot.position + seconds * robot.velocity)

        self.simulated += seconds

    def get_safety_factor(self):
        robot_positions = [robot.position for robot in self.robots]
        quadrants = [0, 0, 0, 0]

        for y in range(self.height):
            for x in range(self.width):
                robot_count = robot_positions.count(Coord(x, y))

                if x < self.width // 2 and y < self.height // 2:
                    quadrants[0] += robot_count
                if x > self.width // 2 and y < self.height // 2:
                    quadrants[1] += robot_count
                if x < self.width // 2 and y > self.height // 2:
                    quadrants[2] += robot_count
                if x > self.width // 2 and y > self.height // 2:
                    quadrants[3] += robot_count

        return reduce(lambda total, current: total * current, quadrants)

    def save_image(self, path: str):
        pixels = np.full((self.height, self.width, 3), 0, dtype=np.uint8)

        for robot in self.robots:
            x, y = robot.position
            pixels[y, x][0] = 255
            pixels[y, x][1] = 255
            pixels[y, x][2] = 255

        new_image = Image.fromarray(pixels)
        new_image.save(os.path.join(path, f"image_{self.simulated}.png"))


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        # map_width, map_height = (11, 7)
        map_width, map_height = (101, 103)
        bathroom_map = BathroomMap(["." * map_width] * map_height, file.read())

        iterations = 10000
        fill = len(str(iterations))
        for i in range(iterations):
            bathroom_map.simulate(1)
            bathroom_map.save_image(os.path.join("2024", "day14", "temp"))
            if i == 100:
                print(f"The safety factor is {bathroom_map.get_safety_factor()}.")
            print(f"{i + 1:<{fill}}/{iterations:<{fill}}", end="\r")


if __name__ == "__main__":
    main()
