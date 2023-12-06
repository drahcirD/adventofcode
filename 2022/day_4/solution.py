#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            [y.split("-") for y in x.split(",")] for x in path.read_text().split("\n")
        ]
        return lines

    def solve(data):
        pairs = 0
        for pair in data:
            left, right = pair
            left = set(range(int(left[0]), int(left[1]) + 1))
            right = set(range(int(right[0]), int(right[1]) + 1))
            if left & right == left or left & right == right:
                pairs += 1
        return pairs

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [
            [y.split("-") for y in x.split(",")] for x in path.read_text().split("\n")
        ]
        return lines

    def solve(data):
        pairs = 0
        for pair in data:
            left, right = pair
            left = set(range(int(left[0]), int(left[1]) + 1))
            right = set(range(int(right[0]), int(right[1]) + 1))
            if left & right != set():
                pairs += 1
        return pairs

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
