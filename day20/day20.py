"""
Advent of Code Day 20
"""

import sys
from math import lcm


class Module:
    label: str
    outputs: list[str]

    def __init__(self, label: str, outputs: list[str]):
        self.label = label
        self.outputs = outputs
        self.cycle = 0
        self.first = 0

    def pulse(self, source: str, value: int) -> list[tuple[str, int]]:
        pass

    def reset(self):
        pass


class FlipFlop(Module):
    value = 0
    previous = 0

    def pulse(self, _, value: int) -> list[tuple[str, int]]:
        if value == 1:
            return []
        self.previous = self.value
        self.value = 1 - self.value
        length = len(self.outputs)
        return zip(self.outputs, [self.label] * length, [self.value] * length)

    def reset(self):
        self.value = 0


class Conjunction(Module):
    inputs: dict[str, int]

    def __init__(self, label: str, outputs: list[str]):
        super().__init__(label, outputs)
        self.inputs = {}

    def pulse(self, source: str, value: int) -> list[tuple[str, int]]:
        self.inputs[source] = value
        length = len(self.outputs)
        if all([input == 1 for _, input in self.inputs.items()]):
            return zip(self.outputs, [self.label] * length, [0] * length)
        else:
            return zip(self.outputs, [self.label] * length, [1] * length)

    def reset(self):
        for key in self.inputs.keys():
            self.inputs[key] = 0


class Broadcast(Module):
    def pulse(self, _, value: int) -> list[tuple[str, int]]:
        length = len(self.outputs)
        return zip(self.outputs, [self.label] * length, [value] * length)


def main():
    with open(sys.argv[1], encoding="utf-8") as file:
        lines = file.read().splitlines()
        modules: dict[str, Module] = {}

        for line in lines:
            label, outputs = line.split(" -> ")
            outputs = outputs.split(", ")

            if label == "broadcaster":
                modules[label] = Broadcast(label, outputs)
            elif label[0] == "%":
                modules[label[1:]] = FlipFlop(label[1:], outputs)
            elif label[0] == "&":
                modules[label[1:]] = Conjunction(label[1:], outputs)

        for key, module in modules.items():
            for output in module.outputs:
                if (
                    output in modules
                    and output != key
                    and isinstance(modules[output], Conjunction)
                ):
                    conjunction: Conjunction = modules[output]
                    conjunction.inputs[key] = 0

        pulses = [0, 0]

        for _ in range(1000):
            queue = [("broadcaster", None, 0)]

            while len(queue) > 0:
                module, source, value = queue.pop(0)
                pulses[value] += 1

                if module in modules:
                    queue.extend(modules[module].pulse(source, value))

        print(f"The product of the pulses is {pulses[0] * pulses[1]}")

        for key, module in modules.items():
            module.reset()

        button_press = 0
        cycle = 0
        collector: Conjunction = modules["vf"]
        cycles: dict[str, int] = {}

        while True:
            queue = [("broadcaster", None, 0)]
            cycle += 1

            while len(queue) > 0:
                module, source, value = queue.pop(0)

                if module == "vf" and value == 1:
                    cycles[source] = cycle

                if module in modules:
                    queue.extend(modules[module].pulse(source, value))

            if all([input in cycles for input in collector.inputs]):
                break

        button_press = lcm(*cycles.values())

        print(
            f"The button presses needed to send a low pulse to the 'rx' module is {button_press}"
        )


if __name__ == "__main__":
    main()
