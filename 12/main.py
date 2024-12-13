from collections import defaultdict, deque
from typing import List, NamedTuple, Set


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> List["Point"]:
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x, self.y + 1)

def regions(plots: Set[Point]) -> Set[Point]:
    while plots:
        initial = plots.pop()
        queue = deque([initial])
        region = {initial}
        while queue:
            plot = queue.popleft()
            for neighbor in plot.neighbors():
                if neighbor in plots:
                    queue.append(neighbor)
                    region.add(neighbor)
                    plots.remove(neighbor)
        yield region

def part1(lines: List[str]):
    lines = [['.']+list(l) + ['.'] for l in lines]
    lines.insert(0, ['.']*len(lines[0]))
    lines.append(['.']*len(lines[0]))
    plots = defaultdict(set)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                plots[char].add(Point(x, y))
    total = 0
    for crop, plot in plots.items():

        for region in regions(plot.copy()):
            perimeter = 0
            for spot in region:
                for neighbor in spot.neighbors():
                    if lines[neighbor.y][neighbor.x] != crop:
                        perimeter += 1
            # print(crop, len(region), perimeter, len(plot)* perimeter)
            total += len(region) * perimeter
    return total

def part2(lines: List[str]):
    return

if __name__ == '__main__':
    with open("test01") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")