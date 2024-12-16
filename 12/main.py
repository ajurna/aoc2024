from collections import defaultdict, deque
from typing import List, NamedTuple, Set, Generator


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> Generator["Point"]:
        yield self.up()
        yield self.down()
        yield self.left()
        yield self.right()

    def up(self):
        return Point(self.x, self.y - 1)
    def down(self):
        return Point(self.x, self.y + 1)
    def left(self):
        return Point(self.x - 1, self.y)
    def right(self):
        return Point(self.x + 1, self.y)

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
    lines = [['.'] + list(l) + ['.'] for l in lines]
    lines.insert(0, ['.'] * len(lines[0]))
    lines.append(['.'] * len(lines[0]))
    plots = defaultdict(set)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                plots[char].add(Point(x, y))
    total = 0
    for crop, plot in plots.items():

        for region in regions(plot.copy()):
            perimeter = set()
            wall_count = 0
            for spot in region:
                for neighbor in spot.neighbors():
                    if lines[neighbor.y][neighbor.x] != crop:
                        perimeter.add(neighbor)
            # print("H:", get_horizontal_walls(region, perimeter))
            # print("V:", get_vertical_walls(region, perimeter))
            wall_count += get_horizontal_walls(region, perimeter)
            wall_count += get_vertical_walls(region, perimeter)
            total += wall_count * len(region)
            # print(crop, len(region), wall_count)
    return total

def get_horizontal_walls(region, perimeter):
    perimeter_up = perimeter.copy()
    perimeter_down = perimeter.copy()
    total = 0
    while perimeter_up:
        p = perimeter_up.pop()
        if p.up() in region:
            queue = deque([p])
            while queue:
                q = queue.popleft()
                right = q.right()
                left = q.left()
                if right in perimeter_up and right.up() in region:
                    perimeter_up.remove(right)
                    queue.append(right)
                if left in perimeter_up and left.up() in region:
                    perimeter_up.remove(left)
                    queue.append(left)
            total += 1
    while perimeter_down:
        p = perimeter_down.pop()
        if p.down() in region:
            queue = deque([p])
            while queue:
                q = queue.popleft()
                right = q.right()
                left = q.left()
                if right in perimeter_down and right.down() in region:
                    perimeter_down.remove(right)
                    queue.append(right)
                if left in perimeter_down and left.down() in region:
                    perimeter_down.remove(left)
                    queue.append(left)
            total += 1
    return total

def get_vertical_walls(region, perimeter):
    perimeter_right = perimeter.copy()
    perimeter_left = perimeter.copy()
    total = 0
    while perimeter_right:
        p = perimeter_right.pop()
        if p.right() in region:
            queue = deque([p])
            while queue:
                q = queue.popleft()
                up = q.up()
                down = q.down()
                if up in perimeter_right and up.right() in region:
                    perimeter_right.remove(up)
                    queue.append(up)
                if down in perimeter_right and down.right() in region:
                    perimeter_right.remove(down)
                    queue.append(down)
            total += 1
    while perimeter_left:
        p = perimeter_left.pop()
        if p.left() in region:
            queue = deque([p])
            while queue:
                q = queue.popleft()
                up = q.up()
                down = q.down()
                if up in perimeter_left and up.left() in region:
                    perimeter_left.remove(up)
                    queue.append(up)
                if down in perimeter_left and down.left() in region:
                    perimeter_left.remove(down)
                    queue.append(down)
            total += 1
    return total

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")