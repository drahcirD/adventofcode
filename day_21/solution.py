#! /usr/bin/env python
import pathlib
import fire
import sympy

def e1(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p1(path)

def e2(path = pathlib.Path(__file__).resolve().parent / "example.txt"):
    return p2(path)

def p1(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split('\n')]
        res = {}
        for line in lines:
            line = line.split(':')
            res[line[0]] = line[1].lstrip().split(' ')
        return res
        
    def solve(data):
        def calc(graph, key):
            cur = graph[key]
            if len(cur) > 1:
                match cur[1]:
                    case '+':
                        graph[key] = calc(graph, cur[0]) + calc(graph, cur[2]) 
                    case '-':
                        graph[key] = calc(graph, cur[0]) - calc(graph, cur[2]) 
                    case '*':
                        graph[key] = calc(graph, cur[0]) * calc(graph, cur[2]) 
                    case '/':
                        graph[key] = calc(graph, cur[0]) / calc(graph, cur[2])
            else:
                graph[key] = int(cur[0])
            return graph[key]
        
        res = calc(data, 'root')
        return res
    
    return solve(parse())

def p2(path = pathlib.Path(__file__).resolve().parent / "input.txt"):
    def parse():
        lines = [x for x in path.read_text().split('\n')]
        res = {}
        for line in lines:
            line = line.split(':')
            res[line[0]] = line[1].lstrip().split(' ')
            if line[0] == 'root':
                res[line[0]][1] = '=='
        return res
        
    def solve(data):
        def calc(graph, key):
            cur = graph[key]
            if len(cur) > 1:
                graph[key] = f"({calc(graph, cur[0])}){cur[1]}({calc(graph, cur[2])})"
    
            else:
                if key != "humn":
                    graph[key] = int(cur[0])
                else:
                    graph[key] = 'X'
            return graph[key]
        
        res = calc(data, 'root').split('==')
        eq = sympy.sympify(f"{res[0]}-{res[1]}")
        return sympy.solve(eq)
    
    return solve(parse())

def main():
    example = pathlib.Path(__file__).resolve().parent / "example.txt"
    return {
        "part1": {"example": p1(example), "input": p1()},
        "part2": {"example": p2(example), "input": p2()},
    }


if __name__ == '__main__':
  fire.Fire()
    
    