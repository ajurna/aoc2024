from collections import deque
from itertools import zip_longest
from typing import List, NamedTuple

class File(NamedTuple):
    id: int

    def __repr__(self):
        return str(self.id)

def part1(lines: List[str]):
    data = list(map(int, lines[0]))
    disk = deque()
    current_id = 0
    for f, s in zip_longest(data[0::2], data[1::2], fillvalue=0):
        for _ in range(f):
            disk.append(File(current_id))
        current_id += 1
        for _ in range(s):
            disk.append(None)
    new_disk = list()
    while disk:
        item = disk.popleft()
        if item:
            new_disk.append(item)
        else:
            end_item = None
            while not end_item:
                if len(disk)> 0:
                    end_item = disk.pop()
                else:
                    break
            if end_item:
                new_disk.append(end_item)
    total = 0
    for x, item in enumerate(new_disk):
        total += item.id * x
    return total

def part2(lines: List[str]):
    data = list(map(int, lines[0]))
    disk = list()
    current_id = 0
    size = {}
    space = {}
    for f, s in zip_longest(data[0::2], data[1::2], fillvalue=0):
        disk.append(File(current_id))
        size[current_id] = f
        space[current_id] = s
        current_id += 1
    for x in range(current_id-1, 0,-1):
        for i, y in enumerate(disk[:disk.index(File(x))]):
            if space[y.id] >= size[x]:
                file_to_move = File(x)
                file_to_move_index = disk.index(file_to_move)
                space[disk[file_to_move_index-1].id] += size[x] + space[x]
                disk.remove(file_to_move)
                disk.insert(i+1, file_to_move)
                space[x] = space[y.id] - size[x]
                space[y.id] = 0
                break
    new_disk = list()
    for item in disk:
        for x in range(size[item.id]):
            new_disk.append(item.id)
        for x in range(space[item.id]):
            new_disk.append(0)
    total = 0
    for x, item in enumerate(new_disk):
        total += item * x

    return total


if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")