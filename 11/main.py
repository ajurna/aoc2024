from collections import deque
from functools import cache
from typing import List


def part1(lines: List[str]):
    stones = deque(map(int, lines[0].split()))
    for _ in range(25):
        for _ in range(len(stones)):
            stone = stones.popleft()
            if stone == 0:
                stones.append(1)
                continue
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                stones.append(int(stone_str[:len(stone_str) // 2]))
                stones.append(int(stone_str[len(stone_str) // 2:]))
                continue
            stones.append(stone * 2024)
    return len(stones)

def blink(stone: int) -> List[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        return [int(stone_str[:len(stone_str) // 2]), int(stone_str[len(stone_str) // 2:])]
    return [stone * 2024]

@cache
def count_stones(stone, blinks):
    if blinks == 0:
        return 1
    count = 0
    for new_stone in blink(stone):
        count += count_stones(new_stone, blinks-1)
    return count


def part2(lines: List[str]):
    count = 0
    for stone in map(int, lines[0].split()):
        count += count_stones(stone, 75)
    return count

if __name__ == '__main__':
    with open("input") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")