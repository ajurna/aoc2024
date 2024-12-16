from typing import List, NamedTuple
import re


class Point(NamedTuple):
    x: int
    y: int
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Robot(NamedTuple):
    location: Point
    x_velocity: int
    y_velocity: int

    def step(self, time, x_max=101, y_max=103):
        return Point((self.location.x + time * self.x_velocity)%x_max, (self.location.y + time * self.y_velocity)%y_max)

def get_robots(lines: List[str]) -> List[Robot]:
    reg = re.compile(r'p=(?P<x>\d+),(?P<y>\d+) v=(?P<x_v>-?\d+),(?P<y_v>-?\d+)')
    robots = []
    for line in reg.findall(''.join(lines)):
        robots.append(
            Robot(
                Point(int(line[0]), int(line[1])),
                int(line[2]),
                int(line[3]),
            )
        )
    return robots

def part1(lines: List[str]):
    # x_max = 11
    # y_max = 7
    x_max = 101
    y_max = 103
    robots = get_robots(lines)
    # area = [['.'] * 11 for _ in range(7)]
    positions = []
    for position in [x.step(100, x_max, y_max) for x in robots]:
        # area[position.y][position.x] = '#'
        positions.append(position)
    # for line in area:
    #     print(''.join(line))
    tl, tr, bl, br = 0, 0, 0, 0
    for position in positions:
        if position.x < x_max//2 and position.y < y_max//2:
            tl += 1
        elif position.x > x_max//2 and position.y < y_max//2:
            tr += 1
        elif position.x < x_max//2 and position.y > y_max//2:
            bl += 1
        elif position.x > x_max//2 and position.y > y_max//2:
            br += 1
    return tl * tr * bl * br



def part2(lines: List[str]):
    return

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")