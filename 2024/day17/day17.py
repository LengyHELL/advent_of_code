"""
Advent of Code Day 17
"""

import sys
import re
from typing import Dict, Callable, List


class Machine:
    register_a: int
    register_b: int
    register_c: int
    pointer: int
    instructions: Dict[int, Callable[[int], None | int]]

    def __init__(self, a: int = 0, b: int = 0, c: int = 0):
        self.register_a = a
        self.register_b = b
        self.register_c = c
        self.pointer = 0

        self.instructions = {
            0: self.__adv,
            1: self.__bxl,
            2: self.__bst,
            3: self.__jnz,
            4: self.__bxc,
            5: self.__out,
            6: self.__bdv,
            7: self.__cdv,
        }

    def __literal(self, value: int):
        return value

    def __combo(self, value: int):
        if value <= 3:
            return value
        elif 4 <= value <= 6:
            return (self.register_a, self.register_b, self.register_c)[value - 4]
        else:
            return 0

    def __adv(self, param: int):
        operand = self.__combo(param)
        self.register_a = self.register_a // 2**operand

    def __bxl(self, param: int):
        operand = self.__literal(param)
        self.register_b = self.register_b ^ operand

    def __bst(self, param: int):
        operand = self.__combo(param)
        self.register_b = operand % 8

    def __jnz(self, param: int):
        if self.register_a == 0:
            return
        operand = self.__literal(param)
        self.pointer = operand - 2

    def __bxc(self, _: int):
        self.register_b = self.register_b ^ self.register_c

    def __out(self, param: int):
        operand = self.__combo(param)
        return operand % 8

    def __bdv(self, param: int):
        operand = self.__combo(param)
        self.register_b = self.register_a // 2**operand

    def __cdv(self, param: int):
        operand = self.__combo(param)
        self.register_c = self.register_a // 2**operand

    def run_program(self, program: List[int]):
        output = []
        self.pointer = 0

        while self.pointer < len(program):
            instruction = program[self.pointer]
            param = program[self.pointer + 1]

            value = self.instructions[instruction](param)

            if value is not None:
                output.append(value)

            self.pointer += 2

        return output


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        a, b, c, values = re.match(
            r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([\d,]+)",
            file.read(),
        ).groups()
        program = list(map(int, values.strip().split(",")))
        machine = Machine(int(a), int(b), int(c))
        output = ",".join(map(str, machine.run_program(program)))

        print(f"The output of the program is '{output}'.")

        register = 0
        for i in range(len(program)):
            while True:
                machine.register_a = register
                machine.register_b = 0
                machine.register_c = 0

                output = machine.run_program(program)

                if output[-(i + 1) :] == program[-(i + 1) :]:
                    break

                if len(output) > len(program):
                    break

                register += 8 ** (len(program) - (i + 1))

        print(f"The lowest A register to output a copy is {register}.")


if __name__ == "__main__":
    main()
