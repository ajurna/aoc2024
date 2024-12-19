import math
from collections import deque, defaultdict
from typing import List, NamedTuple
from rich import print
from rich.table import Table

class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def north(self):
        return Point(self.x, self.y-1)
    def south(self):
        return Point(self.x, self.y+1)
    def east(self):
        return Point(self.x+1, self.y)
    def west(self):
        return Point(self.x-1, self.y)
    def neighbors(self, max_x=math.inf, max_y=math.inf):
        north = self.north()
        if 0 <= north.y <= max_y and 0 <= north.x <= max_x:
            yield north
        south = self.south()
        if 0 <= south.y <= max_y and 0 <= south.x <= max_x:
            yield south
        east = self.east()
        if 0 <= east.x <= max_x and 0 <= east.y <= max_y:
            yield east
        west = self.west()
        if 0 <= west.y <= max_y and 0 <= west.x <= max_x:
            yield west

class QueueItem(NamedTuple):
    score: int
    location: Point

def part1(lines: List[str]):
    start = Point(0, 0)
    max_x = 0
    max_y = 0
    blocks = deque()
    for line in lines:
        x , y = map(int, line.split(','))
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        blocks.append(Point(x, y))
    end = Point(max_x, max_y)
    queue = deque([QueueItem(score=0, location=start)])
    walls = set()
    for _ in range(1024):
        walls.add(blocks.popleft())
    scores = defaultdict(lambda :math.inf)
    scores[start] = 0
    while queue:
        item = queue.popleft()
        if item.location == end:
            break
        for neighbour in item.location.neighbors(max_x, max_y):
            if neighbour not in walls and neighbour not in scores:
                scores[neighbour] = min(scores[neighbour], item.score+1)
                queue.append(QueueItem(item.score+1,neighbour))
    return item.score

def a_star(start, end, max_x, max_y, walls):
    scores = defaultdict(lambda: math.inf)
    queue = deque([QueueItem(score=0, location=start)])
    scores[start] = 0
    while queue:
        item = queue.popleft()
        if item.location == end:
            break
        for neighbour in item.location.neighbors(max_x, max_y):
            if neighbour not in walls and neighbour not in scores:
                scores[neighbour] = min(scores[neighbour], item.score + 1)
                queue.append(QueueItem(item.score + 1, neighbour))
    return scores

def print_map(scores, walls, max_x, max_y):
    area = [['.']*(max_x+1) for _ in range(max_y+1)]
    for p, score in scores.items():
        area[p.y][p.x] = score
    for w in walls:
        area[w.y][w.x] = '#'
    grid = Table.grid(expand=True)
    for _ in range(max_x+1):
        grid.add_column(justify='center')
    for line in area:
        grid.add_row(*map(str, line))
    print(grid)

def part2(lines: List[str]):
    start = Point(0, 0)
    max_x = 0
    max_y = 0
    blocks = deque()
    for line in lines:
        x, y = map(int, line.split(','))
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        blocks.append(Point(x, y))
    end = Point(max_x, max_y)
    walls = set()
    for _ in range(1024):
        walls.add(blocks.popleft())
    scores = a_star(start, end, max_x, max_y, walls)
    while scores[end] != math.inf:
        next_block = blocks.popleft()
        walls.add(next_block)
        scores = a_star(start, end, max_x, max_y, walls)
    return f"{next_block.x},{next_block.y}"

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")