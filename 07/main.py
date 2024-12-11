from typing import List

def combos(depth, current=None):
    if current is None:
        current = []
    if depth == 1:
        yield current + ['+']
        yield current + ['*']
    else:
        yield from combos(depth - 1, current + ['+'])
        yield from combos(depth - 1, current + ['*'])

def combos2(depth, current=None):
    if current is None:
        current = []
    if depth == 1:
        yield current + ['+']
        yield current + ['*']
        yield current + ['||']
    else:
        yield from combos2(depth - 1, current + ['+'])
        yield from combos2(depth - 1, current + ['*'])
        yield from combos2(depth - 1, current + ['||'])

def part1(lines: List[str]):
    ans = 0
    for line in lines:
        target, parts = line.split(': ')
        target = int(target)
        parts = list(map(int,parts.split(' ')))
        initial = parts.pop(0)
        for combo in combos(len(parts)):
            total = initial
            for val, opr in zip(parts, combo):
                if opr == '+':
                    total += val
                elif opr == '*':
                    total *= val
            if total == target:
                ans += target
                break
    return ans


def part2(lines: List[str]):
    ans = 0
    for line in lines:
        target, parts = line.split(': ')
        target = int(target)
        parts = list(map(int, parts.split(' ')))
        initial = parts.pop(0)
        for combo in combos2(len(parts)):
            total = initial
            for val, opr in zip(parts, combo):
                if opr == '+':
                    total += val
                elif opr == '*':
                    total *= val
                elif opr == '||':
                    total = int(str(total) + str(val))
            if total == target:
                ans += target
                break
    return ans

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")