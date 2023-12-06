#! /usr/bin/env python
from email.policy import default
import pathlib

import fire


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        signal = 0
        x = 1
        cycle = 1
        for instr in data:
            if len(instr) == 2:
                instr, val = instr
                cycle += 1
                if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
                    signal += cycle * x
                    print(cycle, x, signal)
                cycle += 1
                x += int(val)
            else:
                cycle += 1

            if cycle == 20 or (cycle > 20 and (cycle - 20) % 40 == 0):
                signal += cycle * x
                print(cycle, x, signal)

        return signal

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split(" ") for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        x = 1
        cycle = 0
        for instr in data:
            if len(instr) == 2:
                instr, val = instr
                cycle += 1
                pos = cycle % 40
                if cycle % 40 == 0:
                    print()
                if abs(x-pos) <= 1:
                    print('.', sep='', end='')
                else:
                    print(' ', sep='', end='')
                cycle += 1
                x += int(val)
            else:
                cycle += 1

            if cycle % 40 == 0:
                print()
            pos = cycle % 40
            if abs(x-pos) <= 1:
                print('.', sep='', end='')
            else:
                print(' ', sep='', end='')

        print()
        print('='*40)

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
