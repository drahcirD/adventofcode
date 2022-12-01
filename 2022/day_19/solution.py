#! /usr/bin/env python
from collections import deque
from functools import reduce
import operator
import pathlib
import fire
import multiprocessing


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)

def bfs(_id, blueprint, time=24):
    distances = {}
    distances[((0, 0, 0, 0, 1), (1, 0, 0, 0))] = 0

    visited = set()
    pq = deque([((0, 0, 0, 0, 1), (1, 0, 0, 0))])
    max_costs = {resource: 0 for resource in blueprint}
    for robot, costs in blueprint.items():
        for resource, cost in costs.items():
            max_costs[resource] = max(max_costs[resource], cost)
    times = set()
    while pq:
        cur = pq.popleft()
        if cur in visited or cur[0][-1] > time:
            visited.add(cur)
            continue
        if cur[0][-1] not in times:
            print(_id, cur[0][-1])
            times.add(cur[0][-1])
        visited.add(cur)
        new_robots = []
        for robot, costs in blueprint.items():
            robots = list(cur[1])
            match robot:
                case "geode":
                    if cur[0][0] >= costs["ore"] and cur[0][2] >= costs["obsidian"]:
                        robots[3] += 1
                        new_robots= [((costs["ore"], 0, costs["obsidian"], 0), tuple(robots))]
                        break
                case "obsidian":
                    if (
                        cur[1][2] < max_costs["obsidian"]
                        and cur[0][0] >= costs["ore"]
                        and cur[0][1] >= costs["clay"]
                    ):
                        robots[2] += 1
                        new_robots.append(
                            ((costs["ore"], costs["clay"], 0, 0), tuple(robots))
                        )
                case "clay":
                    if cur[1][1] < max_costs["clay"] and cur[0][0] >= costs["ore"]:
                        robots[1] += 1
                        new_robots.append(((costs["ore"], 0, 0, 0), tuple(robots)))
                case "ore":
                    if cur[1][0] < max_costs["ore"] and cur[0][0] >= costs["ore"]:
                        robots[0] += 1
                        new_robots.append(((costs["ore"], 0, 0, 0), tuple(robots)))
                case _:
                    raise ValueError
        if not new_robots:
            # This optimization does not work on e2, but works on input
            new_robots.append(((0, 0, 0, 0), tuple(cur[1])))   

        for cost, robots in new_robots:
            state = list(cur[0])
            state[-1] += 1
            assert cost[3] == 0
            state[3] += cur[1][3] - cost[3]
            state[2] += cur[1][2] - cost[2]
            state[1] += cur[1][1] - cost[1]
            state[0] += cur[1][0] - cost[0]
            neighbor_state = (tuple(state), robots)
            pq.append(neighbor_state)
    return max(visited, key=lambda x: x[0][3])[0][3]

def sub(args):
    _id, blueprint = args
    res = bfs(blueprint, time=24)
    print(_id, res)
    quality = _id * res
    return quality


def sub2(args):
    _id, blueprint = args
    geodes = bfs(_id, blueprint, time=32)
    print(_id, geodes)
    return geodes


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split("\n") for x in path.read_text().split("\n\n")]
        blueprints = {}
        for line in lines[:3]:
            _id = int(line[0].split(" ")[-1][:-1])
            blueprints[_id] = {}
            for robot_line in line[1:]:
                robot_line = robot_line.replace(".", "").split(" ")
                blueprints[_id][robot_line[1]] = {}
                for i in range(4, len(robot_line), 3):
                    blueprints[_id][robot_line[1]][robot_line[i + 1]] = int(
                        robot_line[i]
                    )

        return blueprints

    def solve(data):
        qualities = []
        with multiprocessing.Pool() as p:
            qualities = p.map(sub, data.items())
            return sum(qualities)

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split("\n") for x in path.read_text().split("\n\n")]
        blueprints = {}
        for line in lines[:3]:
            _id = int(line[0].split(" ")[-1][:-1])
            blueprints[_id] = {}
            for robot_line in line[1:]:
                robot_line = robot_line.replace(".", "").split(" ")
                blueprints[_id][robot_line[1]] = {}
                for i in range(4, len(robot_line), 3):
                    blueprints[_id][robot_line[1]][robot_line[i + 1]] = int(
                        robot_line[i]
                    )

        return blueprints

    def solve(data):
        with multiprocessing.Pool() as p:
            geodes = p.map(sub2, data.items())
            print(geodes)
            return reduce(operator.mul, geodes, 1)

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
