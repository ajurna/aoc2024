from itertools import combinations
from typing import List, NamedTuple
from rich.console import Console

console = Console()

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


def part1(lines: List[str]):
    target = ['X', 'M', 'A', 'S']
    y_len = len(lines) - 3
    x_len = len(lines[0]) - 3
    total = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'X':
                targets = [
                    [lines[y][x], lines[y][x + 1], lines[y][x + 2], lines[y][x + 3]] if x < x_len else [], #right
                    [lines[y][x], lines[y][x - 1], lines[y][x - 2], lines[y][x - 3]] if x > 2 else [], #left
                    [lines[y][x], lines[y + 1][x], lines[y + 2][x], lines[y + 3][x]] if y < y_len else [], #down
                    [lines[y][x], lines[y - 1][x], lines[y - 2][x], lines[y - 3][x]] if y > 2 else [], #up
                    [lines[y][x], lines[y - 1][x + 1], lines[y - 2][x + 2], lines[y - 3][x + 3]] if y > 2 and x < x_len else [],  # up right
                    [lines[y][x], lines[y - 1][x - 1], lines[y - 2][x - 2], lines[y - 3][x - 3]] if y > 2 and x > 2 else [],  # up left
                    [lines[y][x], lines[y + 1][x + 1], lines[y + 2][x + 2], lines[y + 3][x + 3]] if y < y_len and x < x_len else [],  # down right
                    [lines[y][x], lines[y + 1][x - 1], lines[y + 2][x - 2], lines[y + 3][x - 3]] if y < y_len and x > 2 else [],  # down left
                ]
                # console.print(targets)
                # console.print(targets.count(target))
                total += targets.count(target)
    return total


def part2(lines: List[str]):
    target = ['M', 'M', 'S', 'S']
    total = 0
    for y in range(1, len(lines)-1):
        for x in range(1, len(lines[0])-1):
            if lines[y][x] == 'A':
                targets = [
                    [lines[y-1][x-1],lines[y+1][x-1],lines[y-1][x+1],lines[y+1][x+1]], # left
                    [lines[y-1][x-1], lines[y-1][x+1], lines[y+1][x-1], lines[y+1][x+1]], # up
                    [lines[y-1][x+1], lines[y+1][x+1], lines[y-1][x-1], lines[y+1][x-1]], # right
                    [lines[y+1][x-1], lines[y+1][x+1], lines[y-1][x-1], lines[y-1][x+1]] # down
                ]
                # console.print(targets)
                if targets.count(target):
                    total += 1

    return total


if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")