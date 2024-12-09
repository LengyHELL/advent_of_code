"""
Advent of Code Day 9
"""

import sys


def get_checksum(file: str):
    identifier = 0
    disk_map: list[str] = []
    for index, block in enumerate(file):
        if index % 2 == 0:
            disk_map.extend([identifier for _ in range(int(block))])
            identifier += 1
        else:
            disk_map.extend(["." for _ in range(int(block))])

    index = 0
    length = len(disk_map)
    while index < length:
        if disk_map[index] == ".":
            disk_map[index] = disk_map.pop()

            while disk_map[-1] == ".":
                disk_map.pop()

            length = len(disk_map)
        index += 1

    checksum = 0
    for index, block in enumerate(disk_map):
        checksum += index * int(block)

    return checksum


def get_last_file(disk_map: list[str], index: int):
    while disk_map[index] == ".":
        index -= 1

    size = 0
    start = index

    while disk_map[start] == disk_map[index]:
        size += 1
        index -= 1

    return (start + 1, size)


def get_free_space(disk_map: str, end, index=0):
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
    identifier = 0
    disk_map: list[str] = []
    for index, block in enumerate(file):
        if index % 2 == 0:
            disk_map.extend([str(identifier) for _ in range(int(block))])
            identifier += 1
        else:
            disk_map.extend(["." for _ in range(int(block))])

    index = len(disk_map) - 1
    while index >= 0:
        file_start, file_size = get_last_file(disk_map, index)
        free_start, free_size = get_free_space(disk_map, index)

        while file_size > free_size and free_start is not None:
            free_start, free_size = get_free_space(
                disk_map, index, free_start + free_size
            )

        if free_start is not None:
            temp = disk_map[:free_start]
            temp.extend(disk_map[file_start - file_size : file_start])
            temp.extend(disk_map[free_start + file_size : free_start + free_size])
            temp.extend(disk_map[free_start + free_size : file_start - file_size])
            temp.extend(disk_map[free_start : free_start + file_size])
            temp.extend(disk_map[file_start:])
            disk_map = temp

        index = file_start - 1 - file_size

    checksum = 0
    for index, block in enumerate(disk_map):
        if block != ".":
            checksum += index * int(block)

    return checksum


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        # print(get_checksum(file.read()))
        print(get_checksum_without_fragments(file.read()))


if __name__ == "__main__":
    main()
