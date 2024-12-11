from typing import List, NamedTuple
from itertools import cycle


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Move(NamedTuple):
    l: Point
    direction:str


def part1(area: List[str]):
    direction_cycle = cycle([Point(0,-1), Point(1,0), Point(0,1), Point(-1, 0)])
    location = Point(0, 0)
    for i, line in enumerate(area):
        if '^' in line:
            location = Point(line.index('^'), i)
    current_direction = next(direction_cycle)
    visited = set()
    y_max = len(area)-1
    x_max = len(area[0])-1
    while 0 <= location.x < x_max and 0 <= location.y < y_max:
        next_location = location + current_direction
        if area[next_location.y][next_location.x] != '#':
            visited.add(next_location)
            location = next_location
        else:
            current_direction = next(direction_cycle)
            next_location = location + current_direction
            if area[next_location.y][next_location.x] != '#':
                visited.add(next_location)
                location = next_location
            else:
                current_direction = next(direction_cycle)
                next_location = location + current_direction
                location = next_location
    return len(visited)

def next_stop(location: Move, area) -> Move:
    match location.direction:
        case 'N':
            path_to_go = [area[y][location.l.x] for y in range(location.l.y, -1, -1)]
            return Move(Point(x=location.l.x, y=location.l.y - path_to_go.index('#') + 1), 'E')
        case 'E':
            path_to_go = area[location.l.y][location.l.x:]
            return Move(Point(location.l.x + path_to_go.index('#') - 1, location.l.y), 'S')
        case 'S':
            path_to_go = [area[y][location.l.x] for y in range(location.l.y, len(area))]
            return Move(Point(location.l.x, location.l.y + path_to_go.index('#') - 1), 'W')
        case 'W':
            path_to_go = area[location.l.y][location.l.x::-1]
            return Move(Point(location.l.x - path_to_go.index('#') + 1, location.l.y), 'N')

def is_cycle(location, area):
    visited = set()
    try:
        while True:
            new_location = next_stop(location, area)
            if new_location in visited:
                return True
            visited.add(new_location)
            location = new_location
    except ValueError:
        return False

def part2(area: List[str]):
    area = [list(line) for line in area]
    directions = cycle(["N", "E", "S", "W"])
    direction_point = {
        'N': Point(0, -1),
        'E': Point(1, 0),
        'S': Point(0, 1),
        'W': Point(-1, 0)
    }
    next_direction = {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N'
    }
    for i, line in enumerate(area):
        if '^' in line:
            location = Move(Point(line.index('^'), i), 'N')
    valid_blocks = set()
    invalid_blocks = set()
    y_max = len(area) - 1
    x_max = len(area[0])- 1
    while 0 <= location.l.x < x_max and 0 <= location.l.y < y_max:
        next_location = Move(location.l + direction_point[location.direction], location.direction)
        if area[next_location.l.y][next_location.l.x] == '#':
            location = Move(location.l, next_direction[location.direction])
            continue
        area[next_location.l.y][next_location.l.x] = '#'
        if next_location.l not in invalid_blocks and is_cycle(location, area):
            valid_blocks.add(next_location.l)
        else:
            invalid_blocks.add(next_location.l)
        area[next_location.l.y][next_location.l.x] = '.'
        location = next_location

    return len(valid_blocks)

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")