import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

def register_init():
    return {
        'A': 0,
        'B': 0,
        'C': 0,
    }
@dataclass
class Computer:
    instruction_pointer: int = 0
    code: List[int] = field(default_factory=list)
    registers: Dict[str, int] = field(default_factory=register_init)
    output: List[int] = field(default_factory=list)

    def get_combo_value(self, val) -> int:
        if val <= 3:
            return val
        elif val == 4:
            return self.registers['A']
        elif val == 5:
            return self.registers['B']
        elif val == 6:
            return self.registers['C']
        else:
            raise ValueError('Invalid value')

    def run_to_end(self):
        while True:
            try:
                inst = Instruction(self.code[self.instruction_pointer])
                opr = self.code[self.instruction_pointer + 1]
            except IndexError:
                return
            match inst:
                case Instruction.ADV:
                    self.registers['A'] = self.registers['A'] // (2**self.get_combo_value(opr))
                case Instruction.BXL:
                    self.registers['B'] = self.registers['B'] ^ opr
                case Instruction.BST:
                    self.registers['B'] = self.get_combo_value(opr) % 8
                case Instruction.JNZ:
                    if self.registers['A'] != 0:
                        self.instruction_pointer = opr - 2
                case Instruction.BXC:
                    self.registers['B'] = self.registers['B'] ^ self.registers['C']
                case Instruction.OUT:
                    self.output.append(self.get_combo_value(opr) % 8)
                case Instruction.BDV:
                    self.registers['B'] = self.registers['A'] // (2 ** self.get_combo_value(opr))
                case Instruction.CDV:
                    self.registers['C'] = self.registers['A'] // (2 ** self.get_combo_value(opr))
            self.instruction_pointer += 2

def parse_input(lines):
    reg = re.compile(r'Register A: (?P<A>\d+)\nRegister B: (?P<B>\d+)\nRegister C: (?P<C>\d+)\n\nProgram: (?P<code>\S+)')
    data = reg.search('\n'.join(lines)).groupdict()

    return Computer(
        instruction_pointer=0,
        code=list(map(int, data['code'].split(','))),
        registers={
            'A': int(data['A']),
            'B': int(data['B']),
            'C': int(data['C'])
        }
    )

def optimised(a: int):
    # This is not a generic solution and will probably only work for my problem statement.
    out = []
    a = a
    while a > 0:
        b = (a % 8) ^ 1
        c = a // (2 ** b)
        b = b ^ c ^ 4
        a = a // 8
        out.append(b % 8)
    return out[::-1]

def part1(lines: List[str]):
    computer = parse_input(lines)
    computer.run_to_end()
    return ','.join(map(str, computer.output))


def search(total, idx, target):
    i = 0
    while True:
        op = optimised(total+i)
        if op == target:
            return total + i
        if op == target[:len(op)]:
            if result := search((total+i)*8, idx+1, target):
                return result
            else:
                i+=1
                continue
        elif idx > 0 and op[-2] != target[:len(op)][-2]:
            return None
        else:
            i += 1


def part2(lines: List[str]):
    target = [2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0]
    return search(1, 0, target[::-1])


if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
