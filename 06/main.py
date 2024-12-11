from typing import List, NamedTuple
from itertools import cycle
from unittest import case


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
    # visited.add(location)
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
    return len(visited), visited

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
    ordered_visited = []
    try:
        while True:
            new_location = next_stop(location, area)
            if new_location in visited:
                return True
            visited.add(new_location)
            ordered_visited.append(new_location)
            location = new_location
    except ValueError:
        return False

def part2(area: List[str], vis):
    area = [list(line) for line in area]
    direction_cycle = cycle([Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)])
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
    current_direction = next(directions)
    valid_blocks = set()
    y_max = len(area) - 1
    x_max = len(area[0])- 1
    start = location.l
    while 0 <= location.l.x < x_max and 0 <= location.l.y < y_max:
        next_location = Move(location.l + direction_point[location.direction], location.direction)
        # print(location)
        if area[next_location.l.y][next_location.l.x] == '#':
            location = Move(location.l, next_direction[location.direction])
            continue
        # if next_location.l == start:
        #     location = next_location
        #     continue
        area[next_location.l.y][next_location.l.x] = '#'
        if is_cycle(location, area):
            valid_blocks.add(next_location.l)
        area[next_location.l.y][next_location.l.x] = '.'
        location = next_location

    # for line in area:
    #     print(''.join(line))
    print(len(valid_blocks), start in valid_blocks)
    return len(valid_blocks)

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    p1, vis = part1(lines)
    print(f"Part 1: {p1}")
    print(f"Part 2: {part2(lines, vis)}")