from typing import List

def is_safe(report):
    if 0 in report:
        return False
    if not all([-3 <= x <= 3 for x in report]):
        return False
    if not (all([x > 0 for x in report]) or all([x < 0 for x in report])):
        return False
    return True

def prep_data(report):
    return[x - y for x, y in list(zip(report[:-1], report[1:]))]

def part1(lines: List[str]):
    safe_reports = 0
    for line in lines:
        line = list(map(int, line.split()))
        data= prep_data(line)
        if is_safe(data):
            safe_reports += 1
    return safe_reports


def part2(lines: List[str]):
    safe_reports = 0
    for line in lines:
        line = list(map(int, line.split()))
        data = prep_data(line)
        if is_safe(data):
            safe_reports += 1
            continue
        for i in range(len(line)):
            new_line = line.copy()
            new_line.pop(i)
            data = prep_data(new_line)
            if is_safe(data):
                safe_reports += 1
                break

    return safe_reports

if __name__ == '__main__':
    with open("input") as f:
        lines = f.readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")