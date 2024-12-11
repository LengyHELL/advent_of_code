"""
Advent of Code Day 9
"""

import sys


def read_disk_map(file: str):
    identifier = 0
    disk_map: list[str] = []
    for index, block in enumerate(file):
        if index % 2 == 0:
            disk_map.extend([str(identifier) for _ in range(int(block))])
            identifier += 1
        else:
            disk_map.extend(["." for _ in range(int(block))])

    return disk_map


def calculate_checksum(disk_map: list[str]):
    checksum = 0
    for index, block in enumerate(disk_map):
        if block != ".":
            checksum += index * int(block)
    return checksum


def get_checksum(file: str):
    disk_map = read_disk_map(file)

    index = 0
    length = len(disk_map)
    while index < length:
        if disk_map[index] == ".":
            disk_map[index] = disk_map.pop()

            while disk_map[-1] == ".":
                disk_map.pop()

            length = len(disk_map)
        index += 1

    return calculate_checksum(disk_map)


def get_last_file(disk_map: list[str], index: int):
    while disk_map[index] == ".":
        index -= 1

    size = 0
    start = index

    while disk_map[start] == disk_map[index]:
        size += 1
        index -= 1

    return (start + 1, size)


def get_free_space(disk_map: list[str], end: int, index=0):
    current = index
    start = None
    size = 0

    while current < end and (start is None or disk_map[current] == "."):
        if disk_map[current] == ".":
            if start is None:
                start = current
            size += 1
        current += 1

    return (start, size)


def get_checksum_without_fragments(file: str):
    disk_map = read_disk_map(file)

    index = len(disk_map) - 1
    while index >= 0:
        print(f"{index:<20}", end="\r")
        file_start, file_size = get_last_file(disk_map, index)
        free_start, free_size = get_free_space(disk_map, index)

        while file_size > free_size and free_start is not None:
            free_start, free_size = get_free_space(
                disk_map, index, free_start + free_size
            )

        if free_start is not None:
            temp = disk_map[free_start : free_start + file_size]
            disk_map[free_start : free_start + file_size] = disk_map[
                file_start - file_size : file_start
            ]
            disk_map[file_start - file_size : file_start] = temp

        index = file_start - 1 - file_size

    return calculate_checksum(disk_map)


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        disk_map = file.read()

        print(f"The resulting filesystem checksum is {get_checksum(disk_map)}.")
        print(
            f"The resulting filesystem checksum without fragmentation is {get_checksum_without_fragments(disk_map)}."
        )


if __name__ == "__main__":
    main()
