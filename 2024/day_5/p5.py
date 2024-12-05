#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np
import functools
from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n\n")]
    rules, printers = lines
    rules = rules.split("\n")
    printers = printers.split("\n")
    rules2 = collections.defaultdict(set)
    for rule in rules:
        x, y = rule.split("|")
        rules2[int(x)].add(int(y))
    return rules2, printers


def cmp(x, y, rules):
    if x not in rules and y not in rules:
        return 0

    if y in rules.get(x, set()):
        return -1

    if x in rules.get(y, set()):
        return 1

    return 0


def p1(data=aoc_data):
    rules, printers = parse(data)

    result = 0
    for p in printers:
        p = [int(x) for x in p.split(",")]
        psort = sorted(
            p, key=functools.cmp_to_key(lambda x, y, rules=rules: cmp(x, y, rules))
        )

        for val, val2 in zip(p, psort):
            if val != val2:
                break
        else:
            assert len(p) % 2 == 1
            result += int(psort[len(psort) // 2])

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    rules, printers = data
    total = 0
    result = 0
    for p in printers:
        p = [int(x) for x in p.split(",")]
        psort = sorted(
            p, key=functools.cmp_to_key(lambda x, y, rules=rules: cmp(x, y, rules))
        )

        for val, val2 in zip(p, psort):
            if val != val2:
                break
        else:
            assert len(p) % 2 == 1
            result += int(psort[len(psort) // 2])

        total += int(psort[len(psort) // 2])

    return total - result


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


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
