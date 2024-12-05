"""
Advent of Code Day 5
"""

import sys
import re
import functools


def get_deps(pages: list[str], page: str, rules: list[str]):
    before = []
    after = []

    for rule in rules:
        first, second = re.match(r"(\d+)\|(\d+)", rule).groups()

        if page == first:
            after.append(second)
        elif page == second:
            before.append(first)

    return (
        filter(lambda item: item in pages, before),
        filter(lambda item: item in pages, after),
    )


def comparator(rules):
    return lambda left, right: 1 if f"{left}|{right}" in rules else -1


with open(sys.argv[1], encoding="utf-8") as file:
    rules_data, updates_data = file.read().split("\n\n")
    rules = rules_data.split("\n")
    updates = updates_data.split("\n")
    sum_of_page_numbers = 0
    sum_of_corrected_page_numbers = 0

    for update in updates:
        pages = update.split(",")
        correct = True

        for i, page in enumerate(pages):
            before, after = get_deps(pages, page, rules)

            if any(pages.index(b) > i for b in before) or any(
                pages.index(a) < i for a in after
            ):
                correct = False
                break

        if correct:
            sum_of_page_numbers += int(pages[int((len(pages) - 1) / 2)])
        else:
            pages.sort(key=functools.cmp_to_key(comparator(rules)), reverse=True)
            sum_of_corrected_page_numbers += int(pages[int((len(pages) - 1) / 2)])

    print(f"The sum of the page numbers is {sum_of_page_numbers}")
    print(f"The sum of the corrected page numbers is {sum_of_corrected_page_numbers}")
