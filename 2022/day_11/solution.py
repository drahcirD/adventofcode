#! /usr/bin/env python
from dataclasses import dataclass
import functools
import operator
import pathlib

import fire


@dataclass
class Monkey:
    idx: int
    items: list
    operation: str
    test: int
    true: int
    false: int
    inspections: int


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n\n")]
        monkeys = {}
        for line in lines:
            line = line.split("\n")
            idx = int(line[0].split()[1][0])
            items = [int(x) for x in line[1].split(":")[1].strip().split(", ")]
            operation = line[2].split("old")
            if operation[-1]:
                operation = line[2].split("old")[1]
            else:
                operation = line[2].split("old")[1] + "replace"
            test = int(line[3].split(" ")[-1])
            true = int(line[4].split(" ")[-1])
            false = int(line[5].split(" ")[-1])
            monkeys[idx] = Monkey(idx, items, operation, test, true, false, 0)

        return monkeys

    def solve(data):
        for round in range(20):
            for monkey in data.values():
                for i in range(len(monkey.items)):
                    monkey.inspections += 1
                    if "replace" in monkey.operation:
                        op = monkey.operation.replace("replace", str(monkey.items[i]))
                        worry = eval(f"{monkey.items[i]}{op}") // 3
                    else:
                        worry = eval(f"{monkey.items[i]}{monkey.operation}") // 3
                    if worry % monkey.test == 0:
                        data[monkey.true].items.append(worry)
                    else:
                        data[monkey.false].items.append(worry)
                monkey.items = []

        result = sorted([(monkey.inspections, monkey.idx) for monkey in data.values()])
        print(result)
        return result[-1][0] * result[-2][0]

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split("\n\n")]
        monkeys = {}
        for line in lines:
            line = line.split("\n")
            idx = int(line[0].split()[1][0])
            items = [int(x) for x in line[1].split(":")[1].strip().split(", ")]
            operation = line[2].split("old")
            if operation[-1]:
                operation = line[2].split("old")[1].strip().split(" ")
                operation[1] = int(operation[1])
            else:
                operation = [line[2].split("old")[1].strip()]
            test = int(line[3].split(" ")[-1])
            true = int(line[4].split(" ")[-1])
            false = int(line[5].split(" ")[-1])
            monkeys[idx] = Monkey(idx, items, operation, test, true, false, 0)

        return monkeys

    def solve(data):
        mod = functools.reduce(
            operator.mul, [monkey.test for monkey in data.values()], 1
        )
        for round in range(10000):
            print(round)
            for monkey in data.values():
                for i in range(len(monkey.items)):
                    monkey.inspections += 1
                    worry = monkey.items[i]
                    if len(monkey.operation) == 2:
                        op = monkey.operation[0]
                        val = monkey.operation[1]
                    else:
                        op = monkey.operation[0]
                        val = worry

                    match op:
                        case "*":
                            worry *= val
                        case "+":
                            worry += val
                        case "-":
                            worry -= val
                        case "+":
                            worry += val
                        case _:
                            raise ValueError

                    if worry % monkey.test == 0:
                        data[monkey.true].items.append(worry % mod)
                    else:
                        data[monkey.false].items.append(worry % mod)
                monkey.items = []

        result = sorted([(monkey.inspections, monkey.idx) for monkey in data.values()])
        print(result)
        return result[-1][0] * result[-2][0]

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
