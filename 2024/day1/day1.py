"""
Advent of Code Day 1
"""

import sys
import re
import bisect


with open(sys.argv[1], encoding="utf-8") as file:
    list_items = re.findall(r"(\d+)   (\d+)", file.read())
    left_list = []
    right_list = []

    for left_item, right_item in list_items:
        bisect.insort(left_list, int(left_item))
        bisect.insort(right_list, int(right_item))

    if len(left_list) != len(right_list):
        exit("List length mismatch!")

    sum_of_distances = 0
    similarity_score = 0
    for left_item, right_item in zip(left_list, right_list):
        distance = abs(left_item - right_item)
        sum_of_distances += distance
        occurrance = right_list.count(left_item)
        similarity_score += left_item * occurrance

    print(f"The total distance between lists is {sum_of_distances}")
    print(f"The similarity score of the lists is {similarity_score}")
