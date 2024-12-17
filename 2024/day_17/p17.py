#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    registers = []
    for d in data[0].split("\n"):
        registers.append(int(d.split(" ")[-1]))

    program = []
    for d in data[1].split("\n"):
        program.extend([int(x) for x in d.split(" ")[-1].rstrip().split(",")])

    i = 0
    output = []
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        combo = operand if operand < 4 else registers[(operand - 1) % 3]
        match opcode:
            case 0:
                registers[0] = registers[0] // (2**combo)
            case 1:
                registers[1] = registers[1] ^ operand
            case 2:
                registers[1] = combo % 8
            case 3:
                if registers[0] != 0:
                    i = operand
                    continue
            case 4:
                registers[1] ^= registers[2]
            case 5:
                output.append(str(combo % 8))
            case 6:
                registers[1] = registers[0] // (2**combo)
            case 7:
                registers[2] = registers[0] // (2**combo)

        i += 2

    return ",".join(output)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    orig_registers = []
    for d in data[0].split("\n"):
        orig_registers.append(int(d.split(" ")[-1]))

    program = []
    for d in data[1].split("\n"):
        program.extend([int(x) for x in d.split(" ")[-1].rstrip().split(",")])

    last_A = 0
    for n in range(1, len(program) + 1):
        A = last_A << 3
        while True:
            output = []
            a = A
            for _ in range(n):
                b = a % 8
                b ^= 5
                c = a // (2**b)
                b ^= 6
                b ^= c
                output.append(b % 8)
                a = a >> 3

            if tuple(output) == tuple(program[-n:]):
                last_A = A
                break

            A += 1

    return last_A


def main():
    examples = pathlib.Path(__file__).resolve().parent.glob("example*.txt")
    result = collections.defaultdict(dict)
    for example in examples:
        example_data = example.read_text()
        try:
            result["part1"][example.name] = p1(example_data)
        except:
            pass
        try:
            result["part2"][example.name] = p2(example_data)
        except:
            pass

    print()
    print()

    try:
        result["part1"]["input"] = p1(aoc_data)
        result["part2"]["input"] = p2(aoc_data)
    except:
        raise

    pprint(result)

    submit_p1 = input(f'submit p1? {result["part1"]["input"]}')
    if submit_p1.strip().lower() == "y":
        submit(result["part1"]["input"])

    submit_p2 = input(f'submit p2? {result["part2"]["input"]}')
    if submit_p2.strip().lower() == "y":
        submit(result["part2"]["input"])


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path.read_text())


def e2(path=pathlib.Path(__file__).resolve().parent / "example2.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
