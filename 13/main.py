from typing import List, NamedTuple
import re
class Button(NamedTuple):
    x: int
    y: int

class Machine(NamedTuple):
    x: int
    y: int
    a: Button
    b: Button

def solve_machine(machine: Machine, offset: int = 0) -> int:
    prize = (machine.x + offset, machine.y + offset)
    det = machine.a.x * machine.b.y - machine.a.y * machine.b.x
    a = (prize[0] * machine.b.y - prize[1] * machine.b.x) / det
    b = (machine.a.x * prize[1] - machine.a.y * prize[0]) / det
    if (machine.a.x * a + machine.b.x * b, machine.a.y * a + machine.b.y * b) == (prize[0], prize[1]):
        val = a * 3 + b
        if val.is_integer():
            return int(val)
        else:
            return 0
    return 0



def part1(lines: List[str]):
    reg = re.compile(r'Button A: X\+(?P<a_x>\d+), Y\+(?P<a_y>\d+)\nButton B: X\+(?P<b_x>\d+), Y\+(?P<b_y>\d+)\nPrize: X=(?P<p_x>\d+), Y=(?P<p_y>\d+)')
    total = 0
    for problem in reg.findall("\n".join(lines)):
        ax, ay, bx, by, px, py = problem
        machine = Machine(int(px), int(py), Button(int(ax), int(ay)),Button(int(bx), int(by)))
        total += solve_machine(machine)
    return total

def part2(lines: List[str]):
    reg = re.compile(
        r'Button A: X\+(?P<a_x>\d+), Y\+(?P<a_y>\d+)\nButton B: X\+(?P<b_x>\d+), Y\+(?P<b_y>\d+)\nPrize: X=(?P<p_x>\d+), Y=(?P<p_y>\d+)')
    total = 0
    for problem in reg.findall("\n".join(lines)):
        ax, ay, bx, by, px, py = problem
        machine = Machine(int(px), int(py), Button(int(ax), int(ay)), Button(int(bx), int(by)))
        total += solve_machine(machine, offset=10000000000000)
    return total

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")