from collections import deque
from typing import List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> List["Point"]:
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y - 1)
        yield Point(self.x, self.y + 1)


def part1(lines: List[str]):
    area = [['.']+list(map(int, l))+['.'] for l in lines]
    area.insert(0, ['.']*len(area[0]))
    area.append(['.']*len(area[0]))
    trailheads = []
    for y, line in enumerate(area):
        for x, point in enumerate(line):
            if area[y][x] == 0:
                trailheads.append(Point(x, y))
    scores = {}
    for head in trailheads:
        queue = deque([head])
        visited = set()
        ends = set()
        visited.add(head)
        while queue:
            point = queue.popleft()
            visited.add(point)
            if area[point.y][point.x] == 9:
                ends.add(point)
            next_val = area[point.y][point.x] + 1
            for neighbor in point.neighbors():
                if neighbor in visited:
                    continue
                elif area[neighbor.y][neighbor.x] == next_val:
                    queue.append(neighbor)
        scores[head] = len(ends)
    return sum(scores.values())

def part2(lines: List[str]):
    area = [['.'] + list(map(int, l)) + ['.'] for l in lines]
    area.insert(0, ['.'] * len(area[0]))
    area.append(['.'] * len(area[0]))
    trailheads = []
    for y, line in enumerate(area):
        for x, point in enumerate(line):
            if area[y][x] == 0:
                trailheads.append(Point(x, y))
    scores = {}
    for head in trailheads:
        queue = deque([(head,)])
        visited = set()
        ends = set()
        visited.add(head)
        while queue:
            trail = queue.popleft()
            point = trail[-1]
            visited.add(point)
            if area[point.y][point.x] == 9:
                ends.add(trail)
            next_val = area[point.y][point.x] + 1
            for neighbor in point.neighbors():
                if neighbor in visited:
                    continue
                elif area[neighbor.y][neighbor.x] == next_val:
                    queue.append(trail + (neighbor,))
        scores[head] = len(ends)
    return sum(scores.values())

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")