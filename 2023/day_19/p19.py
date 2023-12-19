#! /usr/bin/env python
from functools import reduce
import operator
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

    result = 0
    flows = {}
    for d in data[0].split("\n"):
        name, rest = d[:-1].split("{")
        instrs = rest.split(",")
        flows[name] = []
        for instr in instrs:
            flows[name].append(instr.split(":"))

    for d in data[1].split("\n"):
        values = d[1:-1].split(",")
        vals = {}
        for val in values:
            k, v = val.split("=")
            vals[k] = int(v)

        flow = "in"
        while True:
            print(flow)
            if flow == "A":
                print("accepted", d)
                result += sum(vals.values())
                break
            elif flow == "R":
                print("rejected", d)

                break
            instrs = flows[flow]
            for instr in instrs:
                if len(instr) > 1:
                    if eval(f"lambda {d[1:-1]}: {instr[0]}")():
                        flow = instr[1]
                        break
                else:
                    flow = instr[0]
                    break

    return result


import copy


def parse2(data):
    return parse(data)


def dfs(flows, equations, cur, eq):
    if len(eq) == 1 and eq[0] == "A":
        return reduce(lambda x, y: x * y.length(), cur.values(), 1)
    elif len(eq) == 1 and eq[0] == "R":
        return 0
    elif len(eq) == 1:
        cur = copy.deepcopy(cur)
        return dfs(flows, equations, cur, eq)

    if any(val is None for val in cur.values()):
        return 0
    res = 0
    for instr in eq:
        if any(val is None for val in cur.values()):
            break
        if len(instr) == 2:
            cur2 = copy.deepcopy(cur)
            var = instr[0][0]

            if instr[0][1] == "<":
                cur2[var] = cur2[var].intersection(ranges.Range(1, int(instr[0][2:])))
                cur[var] = cur[var].intersection(ranges.Range(int(instr[0][2:]), 4001))

            else:
                cur2[var] = cur2[var].intersection(
                    ranges.Range(int(instr[0][2:]) + 1, 4001)
                )
                cur[var] = cur[var].intersection(ranges.Range(1, int(instr[0][2:]) + 1))
            if any(val is None for val in cur2.values()):
                continue

            if instr[1] == "A":
                res += reduce(lambda x, y: x * y.length(), cur2.values(), 1)
                continue
            elif instr[1] == "R":
                continue
            res += dfs(flows, equations, cur2, flows[instr[1]])
        elif len(instr) == 1:
            cur2 = copy.deepcopy(cur)
            if any(val is None for val in cur2.values()):
                continue
            if instr[0] == "A":
                res += reduce(lambda x, y: x * y.length(), cur2.values(), 1)
                continue
            elif instr[0] == "R":
                continue
            res += dfs(flows, equations, cur2, flows[instr[0]])

    return res


import ranges


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    flows = {}
    for d in data[0].split("\n"):
        name, rest = d[:-1].split("{")
        instrs = rest.split(",")
        flows[name] = []
        for instr in instrs:
            flows[name].append(instr.split(":"))

    equations = []
    rng = {var: ranges.Range(1, 4001) for var in {"x", "m", "a", "s"}}
    for instr in flows["in"]:
        if len(instr) == 2:
            q = instr[0]
            rng2 = copy.deepcopy(rng)
            if q[1] == "<":
                rng2[q[0]] = rng2[q[0]].intersection(ranges.Range(1, int(q[2:])))
                rng[q[0]] = rng[q[0]].intersection(ranges.Range(int(q[2:]), 4001))
            else:
                rng2[q[0]] = rng2[q[0]].intersection(ranges.Range(int(q[2:]) + 1, 4001))
                rng[q[0]] = rng[q[0]].intersection(ranges.Range(1, int(q[2:]) + 1))

            result += dfs(flows, equations, rng2, flows[instr[1]])
        elif len(instr) == 1:
            result += dfs(flows, equations, rng, flows[instr[0]])

    return result


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
