import sys
import re
import os
from urllib.request import build_opener, install_opener, urlopen
from urllib.error import HTTPError


def main():
    output_file = "puzzle_input.txt"

    if not os.path.isfile(os.path.join(sys.argv[2], output_file)):
        try:
            with open(sys.argv[1], encoding="utf-8") as cookie_file:
                year, day = re.match(
                    r".+advent_of_code\\(\d+)\\day(\d+)", sys.argv[2]
                ).groups()
                url = f"https://adventofcode.com/{year}/day/{day}/input"

                opener = build_opener()
                opener.addheaders = [("Cookie", cookie_file.read())]
                install_opener(opener)

                try:
                    with urlopen(url) as response:
                        with open(output_file, "w", encoding="utf-8") as puzzle_file:
                            puzzle_file.write(
                                response.read().decode("utf-8").strip("\n")
                            )

                    print(f"Input file fetched from '{url}'.")
                except HTTPError:
                    print("Input file not found.")
        except FileNotFoundError:
            print("Cookie info file not found.")

    else:
        print("Input already exists, skipping fetch.")


if __name__ == "__main__":
    main()
