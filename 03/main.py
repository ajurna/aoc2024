from itertools import cycle
from typing import List
import re

def part1(lines: List[str]):
    reg = re.compile(r'mul\(\d+,\d+\)')
    total = 0
    for line in lines:
        for mul in (reg.findall(line)):
            a,b = mul.split(',')
            a = int(a[4:])
            b = int(b[:-1])
            total += a * b
    return total

def part2(lines: List[str]):
    reg = re.compile(r'mul\(\d+,\d+\)')
    lines = ''.join(lines)
    code = ''
    e = cycle(("don't()", 'do()'))
    while lines:
        next_to_find = next(e)
        try:
            ind = lines.index(next_to_find)
        except ValueError:
            if next_to_find == "don't()":
                code += lines
            break
        if next_to_find == "do()":
            lines = lines[ind + 4:]
            continue
        elif next_to_find == "don't()":
            code += lines[:ind]
            lines = lines[ind+7:]
    total = 0
    for mul in (reg.findall(code)):
        a, b = mul.split(',')
        a = int(a[4:])
        b = int(b[:-1])
        total += a * b
    return total

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")