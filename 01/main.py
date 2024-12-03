from typing import List


def part1(data):
    col_1 = []
    col_2 = []
    for line in data:
        a,b = line.split()
        col_1.append(int(a))
        col_2.append(int(b))
    total = 0
    for p1,p2 in zip(sorted(col_1),sorted(col_2)):
        total += abs(p1 - p2)
    print(total)


def part2(data):
    col_1 = []
    col_2 = []
    for line in data:
        a, b = line.split()
        col_1.append(int(a))
        col_2.append(int(b))
    total = 0
    counts = {}
    for item in col_1:
        total += item * counts.get(item, col_2.count(item))
    print(total)

if __name__ == '__main__':
    with open("input") as f:
        lines = f.readlines()
    part1(lines)
    part2(lines)