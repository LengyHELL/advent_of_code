"""
Advent of Code Day 24
"""

import sys
import re


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        init_str, ops_str = file.read().split("\n\n")
        init = init_str.splitlines()
        ops = ops_str.splitlines()
        second = ops.copy()
        variables: dict[str, int] = dict()

        for i in init:
            var, val = i.split(": ")
            variables[var] = int(val)

        bin_x = "".join(
            [
                str(f[1])
                for f in sorted(
                    [v for v in variables.items() if v[0].startswith("x")],
                    key=lambda x: x[0],
                    reverse=True,
                )
            ]
        )

        bin_y = "".join(
            [
                str(f[1])
                for f in sorted(
                    [v for v in variables.items() if v[0].startswith("y")],
                    key=lambda x: x[0],
                    reverse=True,
                )
            ]
        )

        index = 0

        while len(ops) > 0:
            try:
                var_a, operation, var_b, out = re.match(
                    r"([a-z\d]+) (AND|OR|XOR) ([a-z\d]+) -> ([a-z\d]+)", ops[index]
                ).groups()

                val = 0
                if operation == "AND":
                    val = variables[var_a] & variables[var_b]
                elif operation == "XOR":
                    val = variables[var_a] ^ variables[var_b]
                elif operation == "OR":
                    val = variables[var_a] | variables[var_b]

                variables[out] = val

                ops.pop(index)
            except KeyError:
                index += 1
            except IndexError:
                index = 0

        final = sorted(
            [v for v in variables.items() if v[0].startswith("z")],
            key=lambda x: x[0],
            reverse=True,
        )

        bin_z = "".join([str(f[1]) for f in final])

        sum = bin(int(bin_x, 2) + int(bin_y, 2))

        print(bin_x)
        print(bin_y)
        print(sum[2:])
        print(bin_z)

        total = 0
        for var, val in final:
            temp = int(var[1:])
            total += val * 2**temp

        print(total)

        with open(
            "2024/day24/temp/output_graph.dot", "w", encoding="utf-8"
        ) as output_file:
            output_file.write("digraph G {\n")
            for o in second:
                var_a, operation, var_b, out = re.match(
                    r"([a-z\d]+) (AND|OR|XOR) ([a-z\d]+) -> ([a-z\d]+)", o
                ).groups()
                output_file.write(f"\t{{{var_a}, {var_b}}} -> {out};\n")
            output_file.write("}\n")

        # fixed the adder circuit manually using graphviz


if __name__ == "__main__":
    main()
