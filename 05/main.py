from collections import defaultdict
from functools import cmp_to_key
from typing import List


def part1(lines: List[str]):
    rules = defaultdict(set)
    while True:
        line = lines.pop(0)
        if not line:
            break
        a,b = line.split('|')
        rules[a].add(b)
    total = 0
    for line in lines:
        data = line.split(',')
        data_sorted = True
        items_passed = set()
        while data:
            current_item = data.pop(0)
            if items_passed.intersection(rules[current_item]):
                data_sorted = False
                break
            items_passed.add(current_item)
        if data_sorted:
            data = line.split(',')
            total += int(data[len(data)//2])
    return total

class Rules:
    def __init__(self, rules):
        self.rules = rules

    def c2k(self, a, b):
        if a in self.rules[b]:
            return 1
        elif b in self.rules[a]:
            return -1
        else:
            return 0


def part2(lines: List[str]):
    rules = defaultdict(set)
    while True:
        line = lines.pop(0)
        if not line:
            break
        a, b = line.split('|')
        rules[a].add(b)
    total = 0
    cmp = Rules(rules)
    for line in lines:
        data = line.split(',')
        if check_sorted(data.copy(), rules):
            continue
        data.sort(key=cmp_to_key(cmp.c2k))
        total += int(data[len(data) // 2])
    return total



def check_sorted(data, rules):
    data_sorted = True
    items_passed = set()
    while data:
        current_item = data.pop(0)
        if items_passed.intersection(rules[current_item]):
            return False
        items_passed.add(current_item)
    return data_sorted


if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines.copy())}")
    print(f"Part 2: {part2(lines)}")