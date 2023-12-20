#! /usr/bin/env python
from functools import reduce
import math
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
    lines = [x for x in data.split("\n")]
    return lines


# broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a
def p1(data=aoc_data):
    data = parse(data)

    result = 0
    pulses = []
    map = {}
    state = {}
    for d in data:
        name, l = d.split(" -> ")
        l = l.split(", ")
        map[name] = l
        if name[0] == "%":
            state[name[1:]] = 0

    for name, l in map.items():
        for entry in l:
            if f"&{entry}" in map:
                if entry not in state:
                    state[entry] = {}
                state[entry][name[1:]] = 0

    counts = {0: 0, 1: 0}

    def translate(map, name):
        if f"%{name}" in map:
            return f"%{name}"
        elif f"&{name}" in map:
            return f"&{name}"
        elif name == "broadcaster":
            return name
        raise ValueError(name)

    for i in range(1000):
        counts[0] += 1
        pulses = collections.deque(
            [("broadcaster", dst, 0) for dst in map["broadcaster"]]
        )

        while pulses:
            src, dst, pulse = pulses.popleft()
            print(src, dst, pulse)
            counts[pulse] += 1

            if f"%{dst}" in map:
                dst_type = "flip"
            elif f"&{dst}" in map:
                dst_type = "conjunction"
            else:
                continue

            if dst_type == "flip" and pulse == 1:
                continue
            elif dst_type == "flip" and pulse == 0:
                if state[dst] == 0:
                    pulses.extend(
                        (dst, new_dest, 1) for new_dest in map[translate(map, dst)]
                    )
                    state[dst] = 1
                else:
                    pulses.extend(
                        (dst, new_dest, 0) for new_dest in map[translate(map, dst)]
                    )
                    state[dst] = 0
            elif dst_type == "conjunction":
                state[dst][src] = pulse
                if all(s == 1 for s in state[dst].values()):
                    pulses.extend(
                        (dst, new_dest, 0) for new_dest in map[translate(map, dst)]
                    )
                else:
                    pulses.extend(
                        (dst, new_dest, 1) for new_dest in map[translate(map, dst)]
                    )

    return reduce(operator.mul, counts.values(), 1)


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0
    pulses = []
    map = {}
    state = {}
    for d in data:
        name, l = d.split(" -> ")
        l = l.split(", ")
        map[name] = l
        if name[0] == "%":
            state[name[1:]] = 0

    for name, l in map.items():
        for entry in l:
            if f"&{entry}" in map:
                if entry not in state:
                    state[entry] = {}
                state[entry][name[1:]] = 0

    def translate(map, name):
        if f"%{name}" in map:
            return f"%{name}"
        elif f"&{name}" in map:
            return f"&{name}"
        elif name == "broadcaster":
            return name
        raise ValueError(name)

    i = 0
    loops_second = {k: list([]) for k in {"rs", "bt", "dl", "fr", "rv"}}
    loops_first = {k: list([]) for k in {"mj", "qs", "rd", "cs"}}

    while True:
        i += 1
        pulses = collections.deque(
            [("broadcaster", dst, 0) for dst in map["broadcaster"]]
        )
        sent = []
        while pulses:
            src, dst, pulse = pulses.popleft()
            if dst == "rx" and pulse == 0:
                return i

            if f"%{dst}" in map:
                dst_type = "flip"
            elif f"&{dst}" in map:
                dst_type = "conjunction"
            else:
                continue

            if dst_type == "flip" and pulse == 1:
                continue
            elif dst_type == "flip" and pulse == 0:
                if state[dst] == 0:
                    pulses.extend(
                        (dst, new_dest, 1) for new_dest in map[translate(map, dst)]
                    )
                    state[dst] = 1
                else:
                    pulses.extend(
                        (dst, new_dest, 0) for new_dest in map[translate(map, dst)]
                    )
                    state[dst] = 0
            elif dst_type == "conjunction":
                state[dst][src] = pulse
                if all(s == 1 for s in state[dst].values()):
                    pulses.extend(
                        (dst, new_dest, 0) for new_dest in map[translate(map, dst)]
                    )
                else:
                    pulses.extend(
                        (dst, new_dest, 1) for new_dest in map[translate(map, dst)]
                    )
        print(i)
        for second in {"bt", "dl", "fr", "rv"}:
            if any(s == 0 for s in state[second].values()):
                loops_second[second].append(i)

        for first in {"mj", "qs", "rd", "cs"}:
            if all(s == 0 for s in state[first].values()):
                loops_first[first].append(i)

        if i % 10000 == 0:
            breakpoint()

        # manually found cycles of {cs: 3821, rd:3943, qs:4001, mj: 3739}
        return math.lcm(3821, 3943, 4001, 3739)


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
