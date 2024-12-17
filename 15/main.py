from collections import deque
from dataclasses import dataclass
from itertools import chain
from typing import List, NamedTuple, Tuple


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def step(self, direction: str) -> "Point":
        match direction:
            case "<":
                return Point(self.x - 1, self.y)
            case ">":
                return Point(self.x + 1, self.y)
            case "^":
                return Point(self.x, self.y - 1)
            case "v":
                return Point(self.x, self.y + 1)

class Box(NamedTuple):
    left: Point
    right: Point

    def step(self, direction: str) -> "Box":
        return Box(self.left.step(direction), self.right.step(direction))

    def h_side(self, direction: str) -> Point:
        if direction == "<":
            return self.left
        elif direction == ">":
            return self.right
        else:
            raise ValueError("direction must be '<' or '>'")

    def v_side(self, direction: str) -> Tuple[Point, Point]:
        if direction == "^":
            return self.left.step('^'), self.right.step('^')
        elif direction == "v":
            return self.left.step('v'), self.right.step('v')
        else:
            raise ValueError("direction must be '^' or 'v'")

def parse_data(lines: List[str]):
    walls = set()
    boxes = set()
    steps = []
    for y, line in enumerate(lines):
        if line.startswith('#'):
            for x, char in enumerate(line):
                match char:
                    case '#':
                        walls.add(Point(x, y))
                    case 'O':
                        boxes.add(Point(x, y))
                    case '@':
                        robot = Point(x, y)
        elif line == '':
            continue
        else:
            steps.append(line)
    return walls, boxes, robot, steps

def parse_data2(lines: List[str]):
    walls = set()
    boxes = set()
    steps = []
    for y, line in enumerate(lines):
        if line.startswith('#'):
            for x, char in enumerate(line):
                match char:
                    case '#':
                        walls.add(Point(x*2, y))
                        walls.add(Point(x * 2 + 1, y))
                    case 'O':
                        boxes.add(Box(Point(x*2, y), Point(x*2 + 1, y)))
                    case '@':
                        robot = Point(x*2, y)
        elif line == '':
            continue
        else:
            steps.append(line)
    return walls, boxes, robot, steps

def draw_area2(walls, boxes, robot):
    max_x = max(w.x for w in walls)+1
    max_y = max(w.y for w in walls)+1
    area = [['.']*max_x for _ in range(max_y)]
    for w in walls:
        area[w.y][w.x] = "#"
    for b in boxes:
        area[b.left.y][b.left.x] = "["
        area[b.right.y][b.right.x] = "]"
    area[robot.y][robot.x] = "@"
    for line in area:
        print("".join(line))

def draw_area(walls, boxes, robot):
    max_x = max(w.x for w in walls) + 1
    max_y = max(w.y for w in walls) + 1
    area = [['.'] * max_x for _ in range(max_y)]
    for w in walls:
        area[w.y][w.x] = "#"
    for b in boxes:
        area[b.y][b.x] = "O"
    area[robot.y][robot.x] = "@"
    for line in area:
        print("".join(line))

def move_boxes(walls, boxes, initial_box, direction):
    current_box = initial_box
    while True:
        next_box = current_box.step(direction)
        if next_box in walls:
            return False
        if next_box in boxes:
            current_box = next_box
        else:
            break
    boxes.remove(initial_box)
    boxes.add(next_box)
    return True

def move_boxes2(walls, boxes, box_index, initial_box, direction):
    current_box = initial_box
    if direction in ["<", ">"]:
        boxes_to_move = [initial_box]
        while True:
            next_point = current_box.h_side(direction).step(direction)
            if next_point in walls:
                return False
            if next_point in box_index:
                current_box = box_index[next_point]
                boxes_to_move.append(current_box)
            else:
                break
        for box in boxes_to_move:
            boxes.remove(box)
            boxes.add(box.step(direction))
        return True
    else:
        boxes_to_move = set()
        queue = deque([initial_box])
        while queue:
            next_box = queue.popleft()
            boxes_to_move.add(next_box)
            for side in next_box.v_side(direction):
                if side in walls:
                    return False
                if side in box_index and box_index[side] not in queue:
                    queue.append(box_index[side])
        for box in boxes_to_move:
            boxes.remove(box)
        for box in boxes_to_move:
            boxes.add(box.step(direction))
        return True



def part1(lines: List[str]):
    walls, boxes, robot, steps = parse_data(lines)
    for step_line in steps:
        for direction in step_line:
            # draw_area(walls, boxes, robot)
            # print(direction)
            next_step = robot.step(direction)
            if next_step in walls:
                continue
            if next_step in boxes:
                if move_boxes(walls, boxes, next_step, direction):
                    robot = next_step
                continue
            robot = next_step
    total = 0
    for box in boxes:
        total += box.x + box.y*100
    return total


def part2(lines: List[str]):
    walls, boxes, robot, steps = parse_data2(lines)
    steps = list(chain(*steps))
    box_index = {}
    for box in boxes:
        box_index[box.left] = box
        box_index[box.right] = box
    for i, direction in enumerate(steps):
        # if i == 89:
        #     print(i)
        # draw_area2(walls, boxes, robot)
        # print(direction, i)
        next_step = robot.step(direction)
        if next_step in walls:
            continue
        if next_step in box_index:
            if move_boxes2(walls, boxes, box_index, box_index[next_step], direction):
                robot = next_step
                box_index = {}
                for box in boxes:
                    box_index[box.left] = box
                    box_index[box.right] = box
            continue
        robot = next_step
    draw_area2(walls, boxes, robot)
    total = 0
    for box in boxes:
        total += box.left.x + box.left.y*100
    return total

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")