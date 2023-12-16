"""
Advent of Code Day 14
"""

import sys
import time


def modify_string(string: str, modify: str, index: int):
    """
    Returns a new string modified at `index` with `modify`
    """
    return string[:index] + modify + string[index + len(modify) :]


def modify_block(block: list[str], point: tuple[int, int], modify: str):
    block[point[0]] = modify_string(block[point[0]], modify, point[1])


def tilt(rows: list[str], axis: int, reverse=False):
    rocks: list[tuple[int, int]] = []
    tilted = rows.copy()

    for row_index, row in enumerate(tilted):
        for column_index, column in enumerate(row):
            if column == "O":
                rocks.append((row_index, column_index))

    rocks.sort(key=lambda pos: pos[axis], reverse=reverse)

    end = -1
    step = -1
    if reverse:
        step = 1

        if axis == 0:
            end = len(tilted)
        else:
            end = len(tilted[0])

    for rock in rocks:
        nxt = list(rock)
        pos = rock

        while True:
            nxt[axis] += step

            if (nxt[axis] == end) or tilted[nxt[0]][nxt[1]] != ".":
                break
            else:
                pos = tuple[int, int](nxt)

        modify_block(tilted, rock, ".")
        modify_block(tilted, pos, "O")
    return tilted


def get_load(rows: list[str]):
    size = len(rows)
    load = 0

    for index, row in enumerate(rows):
        load += row.count("O") * (size - index)

    return load


with open(sys.argv[1], encoding="utf-8") as file:
    rows = file.read().split("\n")
    cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 1000000000
    fill = len(str(cycles))

    tilted = tilt(rows, 0)
    tilted_load = get_load(tilted)

    loads = []
    cycled = rows.copy()
    states = []
    cycled_load = 0

    timer_start = time.time()
    for cycle in range(cycles):
        current = time.time()
        print(
            f"Cycle {cycle + 1:{fill}}/{cycles:{fill}} {time.time() - timer_start:.0f} s",
            end="\r",
        )

        cycled = tilt(cycled, 0)
        cycled = tilt(cycled, 1)
        cycled = tilt(cycled, 0, True)
        cycled = tilt(cycled, 1, True)

        cycled_load = get_load(cycled)
        if cycled in states:
            index = states.index(cycled)
            pattern = loads[index:]
            cycled_load = pattern[(cycles - cycle - 1) % len(pattern)]
            break
        else:
            states.append(cycled.copy())
            loads.append(cycled_load)

    print(f"\nThe total load on the north support beams is {tilted_load}")
    print(
        f"The total load on the north support beams after {cycles} {'cycle' if cycles < 2 else 'cycles'} is {cycled_load}"
    )
