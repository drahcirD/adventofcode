#! /usr/bin/env python
import functools
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


def dfs(visited, index, node):
    visited.add(node)
    if index >= len(node):
        return

    if node[index] == "?":
        node1 = node[:index] + "#" + node[index + 1 :]
        dfs(visited, index + 1, node1)
        node2 = node[:index] + "." + node[index + 1 :]

        dfs(visited, index + 1, node2)
    elif node[index] in {"#", "."}:
        dfs(visited, index + 1, node)


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    for d in data:
        string, template = d.split(" ")
        template = [int(x) for x in template.split(",")]

        visited = set()

        dfs(visited, 0, string)
        visited = [v for v in visited if "?" not in set(v)]

        r = 0
        for v in visited:
            running_hash = 0
            hash = []
            for i, c in enumerate(v):
                if c == "#":
                    running_hash += 1
                elif c == ".":
                    if running_hash:
                        hash.append(running_hash)
                    running_hash = 0
            if running_hash:
                hash.append(running_hash)
            if hash == template:
                r += 1

        print(string, r)
        result += r

    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)

    result = 0

    @functools.cache
    def dfs2(index, running, filled, t_index):
        if index == len(string):
            if filled == len(template):
                return 1
            else:
                return 0

        if t_index > len(template):
            return 0

        res = 0
        if string[index] == "?":
            res += dfs2(index + 1, running + 1, filled, t_index)

            if t_index < len(template) and running == template[t_index]:
                res += dfs2(index + 1, 0, filled + 1, t_index + 1)
            elif running == 0:
                res += dfs2(index + 1, 0, filled, t_index)

        elif string[index] == "#":
            res += dfs2(index + 1, running + 1, filled, t_index)
        elif string[index] == ".":
            if t_index < len(template) and running == template[t_index]:
                res += dfs2(index + 1, 0, filled + 1, t_index + 1)
            elif running == 0:
                res += dfs2(index + 1, 0, filled, t_index)

        return res

    for d in data:
        string, template = d.split(" ")
        template = [int(x) for x in template.split(",")] * 5
        string = f"{string}?{string}?{string}?{string}?{string}."
        r = dfs2(0, 0, 0, 0)
        dfs2.cache_clear()
        result += r
        print(string, r)
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
        # result["part1"]["input"] = p1(aoc_data)
        result["part2"]["input"] = p2(aoc_data)
    except:
        raise

    pprint(result)

    # submit_p1 = input(f'submit p1? {result["part1"]["input"]}')
    # if submit_p1.strip().lower() == "y":
    #     submit(result["part1"]["input"])

    submit_p2 = input(f'submit p2? {result["part2"]["input"]}')
    if submit_p2.strip().lower() == "y":
        submit(result["part2"]["input"])


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path.read_text())


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path.read_text())


if __name__ == "__main__":
    fire.Fire()
