from collections import defaultdict
from typing import List, NamedTuple, Tuple, Set
from itertools import combinations

class Point(NamedTuple):
    x: int
    y: int

    def anti_nodes(self, other: "Point") -> Tuple["Point", "Point"]:
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        if self.y == other.y:
            return Point(min(self.x, other.x) - x_diff, self.y), Point(max(self.x, other.x) - y_diff, self.y)
        if self.x == other.x:
            return Point(self.x, min(self.y, other.y) - y_diff), Point(self.x, max(self.y, other.y) - x_diff)
        if self.x < other.x:
            if self.y < other.y:
                return Point(self.x - x_diff, self.y - y_diff), Point(other.x + x_diff, other.y + y_diff)
            else:
                return Point(self.x - x_diff, self.y + y_diff), Point(other.x + x_diff, other.y - y_diff)
        else:
            if self.y < other.y:
                return Point(self.x + x_diff, self.y - y_diff), Point(other.x - x_diff, other.y + y_diff)
            else:
                return Point(self.x + x_diff, self.y + y_diff), Point(other.x - x_diff, other.y - y_diff)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def anti_nodes2(self, other: "Point", x_max, y_max) -> Set["Point"]:
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        diff_p = Point(x_diff, y_diff)
        p1 = min(self, other)
        p2 = max(self, other)
        anti_nodes = set()
        anti_nodes.add(p1)
        anti_nodes.add(p2)
        n = p1
        if p2.y > p1.y:
            while True:
                n = n + diff_p
                if n.x >= x_max or n.y >= y_max:
                    break
                anti_nodes.add(n)
            while True:
                n = n - diff_p
                if n.x < 0 or n.y < 0:
                    break
                anti_nodes.add(n)
        else:
            while True:
                n = Point(n.x + diff_p.x, n.y - diff_p.y)
                if n.x >= x_max or n.y >= y_max or n.x < 0 or n.y < 0:
                    break
                anti_nodes.add(n)
            while True:
                n = Point(n.x - diff_p.x, n.y + diff_p.y)
                if n.x >= x_max or n.y >= y_max or n.x < 0 or n.y < 0:
                    break
                anti_nodes.add(n)

        return anti_nodes

def part1(lines: List[str]):
    towers = defaultdict(list)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                towers[c].append(Point(x, y))
    anti_nodes = set()
    for tower, points in towers.items():
        for p1, p2 in combinations(points, 2):
            for node in p1.anti_nodes(p2):
                if 0<= node.x < len(lines[0]) and 0<= node.y < len(lines):
                    anti_nodes.add(node)
    return len(anti_nodes)

def part2(lines: List[str]):
    towers = defaultdict(list)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.':
                towers[c].append(Point(x, y))
    anti_nodes = set()
    for tower, points in towers.items():
        for p1, p2 in combinations(points, 2):
            for node in p1.anti_nodes2(p2, len(lines[0]), len(lines)):
                if 0 <= node.x < len(lines[0]) and 0 <= node.y < len(lines):
                    anti_nodes.add(node)
    return len(anti_nodes)

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")