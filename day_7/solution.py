#! /usr/bin/env python
import pathlib
import fire
import collections
import itertools


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split() for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        dirs = {"/": {}}
        cur_dir = dirs["/"]
        prev_dirs = []
        i = 0
        while i < len(data):
            line = data[i]
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "/":
                        cur_dir = dirs["/"]
                        prev_dirs = []
                    elif line[2] == "..":
                        cur_dir = prev_dirs.pop()
                    else:
                        prev_dirs.append(cur_dir)
                        cur_dir = cur_dir[line[2]]
                elif line[1] == "ls":
                    i += 1
                    line = data[i]
                    while i < len(data) and line[0] != "$":
                        if line[0] == "dir":
                            cur_dir.setdefault(line[1], {})
                        else:
                            cur_dir[line[1]] = int(line[0])
                        if i == len(data) - 1 or data[i + 1][0] == "$":
                            break
                        i += 1
                        line = data[i]

            i += 1
        print(dirs)
        sizes = {}

        def _recurse(sizes, dirs, prev_dir):
            size = 0
            for _dir, content in dirs.items():
                if isinstance(content, dict):
                    sizes[prev_dir + "/" + _dir] = _recurse(
                        sizes, content, prev_dir + "/" + _dir
                    )
                    size += sizes[prev_dir + "/" + _dir]
                else:
                    size += content
            return size

        sizes["/"] = _recurse(sizes, dirs["/"], "")
        print(sizes)
        sum = 0
        for key, val in sizes.items():
            if val <= 100000:
                sum += val
        return sum

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x.split() for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        dirs = {"/": {}}
        cur_dir = dirs["/"]
        prev_dirs = []
        i = 0
        while i < len(data):
            line = data[i]
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] == "/":
                        cur_dir = dirs["/"]
                        prev_dirs = []
                    elif line[2] == "..":
                        cur_dir = prev_dirs.pop()
                    else:
                        prev_dirs.append(cur_dir)
                        cur_dir = cur_dir[line[2]]
                elif line[1] == "ls":
                    i += 1
                    line = data[i]
                    while i < len(data) and line[0] != "$":
                        if line[0] == "dir":
                            cur_dir.setdefault(line[1], {})
                        else:
                            cur_dir[line[1]] = int(line[0])
                        if i == len(data) - 1 or data[i + 1][0] == "$":
                            break
                        i += 1
                        line = data[i]

            i += 1
        sizes = {}

        def _recurse(sizes, dirs, prev_dir):
            size = 0
            for _dir, content in dirs.items():
                if isinstance(content, dict):
                    sizes[prev_dir + "/" + _dir] = _recurse(
                        sizes, content, prev_dir + "/" + _dir
                    )
                    size += sizes[prev_dir + "/" + _dir]
                else:
                    size += content
            return size

        sizes["/"] = _recurse(sizes, dirs["/"], "")
        min = '', 1e99
        for key, val in sizes.items():
            if min[1] > val and 70000000-sizes["/"] + val >= 30000000:
                min = key, val
        return min

    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
