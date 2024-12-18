import sys
import re
import os
from urllib.request import build_opener, install_opener, urlopen
from urllib.error import HTTPError
from termcolor import colored


def main():
    output_file = "puzzle_input.txt"

    if not os.path.isfile(os.path.join(sys.argv[2], output_file)):
        try:
            with open(sys.argv[1], encoding="utf-8") as cookie_file:
                try:
                    year, day = re.match(
                        r".+advent_of_code\\(\d+)\\day(\d+)", sys.argv[2]
                    ).groups()
                except AttributeError:
                    print(
                        colored(
                            "Wrong directory, format must be 'advent_of_code/<year>/day<day>'.",
                            "red",
                        )
                    )
                    sys.exit(4)
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

                    print(colored(f"Input file fetched from '{url}'.", "green"))
                except HTTPError:
                    print(colored("Input file not found.", "red"))
                    sys.exit(3)
        except FileNotFoundError:
            print(colored("Cookie info file not found.", "red"))
            sys.exit(2)

    else:
        print(colored("Input already exists, skipping fetch.", "yellow"))


if __name__ == "__main__":
    main()
