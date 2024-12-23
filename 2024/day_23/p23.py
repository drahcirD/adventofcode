#! /usr/bin/env python
import pathlib
from pprint import pprint
import fire
import collections
import itertools
import more_itertools
import numpy as np
import networkx as nx

from aocd import data as aoc_data
from aocd import submit


def parse(data):
    lines = [x for x in data.split("\n")]
    return lines


def p1(data=aoc_data):
    data = parse(data)

    result = 0

    connections = collections.defaultdict(set)
    for d in data:
        a, b = d.split("-")
        connections[a].add(b)
        connections[b].add(a)

    threeways = set()
    for a, b in itertools.combinations(connections, r=2):
        if a not in connections[b] or b not in connections[a]:
            continue
        c = (connections[a] & connections[b])
        for cc in c:
            if b in connections[cc] and a in connections[cc]:
                threeways.add(tuple(sorted([a, b, cc])))

    for a, b, c in threeways:
        if a[0] == "t" or b[0] == "t" or c[0] == "t":
            result += 1
    return result


def parse2(data):
    return parse(data)


def p2(data=aoc_data):
    data = parse2(data)
    G = nx.Graph()
    for d in data:
        a, b = d.split("-")
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b)
        G.add_edge(b, a)

    return ",".join(sorted(max(nx.find_cliques(G), key=len)))


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
