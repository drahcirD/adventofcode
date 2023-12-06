#! /usr/bin/env python
import pathlib
import fire
import tqdm


def e1(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)


def e2(path=pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)


def p1(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [int(x) for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        old2new = {i: i for i in range(len(data))}
        new2old = {v: k for k, v in old2new.items()}
        for i, x in tqdm.tqdm(enumerate(data)):
            if x > 0:
                x = x % (len(data)-1)
                indices = list(range(old2new[i] + 1, old2new[i] + x + 1))
                for j in indices:
                    new_j = (j-1)% len(data)
                    old = new2old[j%len(data)]
                    old2new[old] = new_j
                    new2old[new_j] = old
                new_i = (old2new[i] + x) % len(data)
                old2new[i] = new_i
                new2old[new_i] = i
                if len(data)+1 in indices:
                    old2new = {k: (v+1)%len(data) for k, v in old2new.items()}
                    new2old = {v: k for k, v in old2new.items()}
            if x < 0:
                x = x % -(len(data)-1)
                indices = list(reversed(range(old2new[i] + x, old2new[i])))
                for j in indices:
                    new_j = (j+1)% len(data)
                    old = new2old[j%len(data)]
                    old2new[old] = new_j
                    new2old[new_j] = old
                new_i = (old2new[i] + x) % len(data)
                old2new[i] = new_i
                new2old[new_i] = i
                if 0 in indices:
                    old2new = {k: (v-1)%len(data) for k, v in old2new.items()}
                    new2old = {v: k for k, v in old2new.items()}
                    
        index = old2new[data.index(0)]
        res = [
            data[new2old[(index+1000) % len(data)]],
            data[new2old[(index+2000) % len(data)]],
            data[new2old[(index+3000) % len(data)]],
        ]
        print(res)
        return sum(res)

    return solve(parse())


def p2(path=pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [int(x) for x in path.read_text().split("\n")]
        return lines

    def solve(data):
        data = [x*811589153 for x in data]
        old2new = {i: i for i in range(len(data))}
        new2old = {v: k for k, v in old2new.items()}
        offset = 0
        for _ in range(10):
            for i, x in enumerate(data):
                if x > 0:
                    x = x % (len(data)-1)
                    indices = list(range(old2new[i] + 1, old2new[i] + x + 1))
                    for j in indices:
                        new_j = (j-1)% len(data)
                        old = new2old[j%len(data)]
                        old2new[old] = new_j
                        new2old[new_j] = old
                    new_i = (old2new[i] + x) % len(data)
                    old2new[i] = new_i
                    new2old[new_i] = i
                    if len(data) in indices:
                        old2new = {k: (v+1)%len(data) for k, v in old2new.items()}
                        new2old = {v: k for k, v in old2new.items()}
                if x < 0:
                    x =  x %-(len(data)-1)
                    indices = list(reversed(range(old2new[i] + x, old2new[i])))
                    for j in indices:
                        new_j = (j+1)% len(data)
                        old = new2old[j%len(data)]
                        old2new[old] = new_j
                        new2old[new_j] = old
                    new_i = (old2new[i] + x) % len(data)
                    old2new[i] = new_i
                    new2old[new_i] = i
                    if 0 in indices:
                        old2new = {k: (v-1)%len(data) for k, v in old2new.items()}
                        new2old = {v: k for k, v in old2new.items()}

        index = old2new[data.index(0)]
        res = [
            data[new2old[(offset+index+1000) % len(data)]],
            data[new2old[(offset+index+2000) % len(data)]],
            data[new2old[(offset+index+3000) % len(data)]],
        ]
        print(res)
        return sum(res)
    return solve(parse())


def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == "__main__":
    fire.Fire()
