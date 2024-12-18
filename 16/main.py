import math
from queue import PriorityQueue
from typing import List, NamedTuple
from enum import Enum

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    @staticmethod
    def turns(direction: "Direction"):
        match direction:
            case Direction.NORTH:
                yield Direction.EAST
                yield Direction.WEST
            case Direction.SOUTH:
                yield Direction.EAST
                yield Direction.WEST
            case Direction.EAST:
                yield Direction.NORTH
                yield Direction.SOUTH
            case Direction.WEST:
                yield Direction.NORTH
                yield Direction.SOUTH

    def __lt__(self, other):
        return self.value < other.value
class Position(NamedTuple):
    x: int
    y: int
    direction: Direction

    def turn(self, direction: Direction):
        return Position(self.x, self.y, direction)

    def step(self):
        match self.direction:
            case Direction.NORTH:
                return Position(self.x, self.y - 1, self.direction)
            case Direction.SOUTH:
                return Position(self.x, self.y + 1, self.direction)
            case Direction.EAST:
                return Position(self.x + 1, self.y, self.direction)
            case Direction.WEST:
                return Position(self.x - 1, self.y, self.direction)

class QueueItem(NamedTuple):
    score: int
    position: Position
    path: tuple

def part1(area: List[str]):
    ends = set()
    area = [list(l) for l in area]
    for y, line in enumerate(area):
        for x, char in enumerate(line):
            if char == 'E':
                for direction in Direction:
                    ends.add(Position(x, y, direction))
            if char == 'S':
                start = Position(x, y, Direction.EAST)
    queue: PriorityQueue = PriorityQueue()

    queue.put(QueueItem(0, start, ()))
    visited = {start}
    while queue:
        item = queue.get()
        if item.position in ends:
            # key = {
            #     Direction.NORTH: "^",
            #     Direction.SOUTH: "v",
            #     Direction.EAST: ">",
            #     Direction.WEST: "<",
            # }
            # for p in item.path:
            #     area[p.y][p.x] = key[p.direction]
            # for line in area:
            #     print("".join(line))
            return item.score
        for direction in Direction.turns(item.position.direction):
            next_position = item.position.turn(direction)
            if next_position in visited:
                continue
            else:
                queue.put(QueueItem(item.score + 1000, Position(item.position.x, item.position.y, direction), item.path + (next_position,)))
                visited.add(next_position)
        next_position = item.position.step()
        if area[next_position.y][next_position.x] != '#' and next_position not in visited:
            queue.put(QueueItem(item.score + 1, next_position, item.path + (next_position,)))

def part2(area: List[str]):
    ends = set()
    area = [list(l) for l in area]
    for y, line in enumerate(area):
        for x, char in enumerate(line):
            if char == 'E':
                for direction in Direction:
                    ends.add(Position(x, y, direction))
            if char == 'S':
                start = Position(x, y, Direction.EAST)
    queue: PriorityQueue = PriorityQueue()
    queue.put(QueueItem(0, start, ()))
    visited = {start}
    min_path = math.inf
    ans = {(start.x, start.y)}
    while queue:
        item = queue.get()
        visited.add(item.position)
        if item.score > min_path:
            return len(ans)
        if item.position in ends:
            if item.score <= min_path:
                min_path = item.score
                for p in item.path:
                    ans.add((p.x, p.y))
            continue
        for direction in Direction.turns(item.position.direction):
            next_position = item.position.turn(direction)
            if next_position in visited:
                continue
            else:
                queue.put(QueueItem(item.score + 1000, Position(item.position.x, item.position.y, direction),
                                    item.path + (next_position,)))
        next_position = item.position.step()
        if area[next_position.y][next_position.x] != '#' and next_position not in visited:
            queue.put(QueueItem(item.score + 1, next_position, item.path + (next_position,)))

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")