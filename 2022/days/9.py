from common import data

instructions = [
    (direction, int(steps))
    for direction, steps in data(9, parser=lambda l: l.split(" "))
]


def touching(head, tail) -> bool:
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1


DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def simulate_movement(instructions, knots) -> int:
    positions = [[0, 0] for _ in range(knots)]
    visited_spaces = set()
    visited_spaces.add(tuple(positions[-1]))
    for direction, steps in instructions:
        movement = DIRECTIONS[direction]
        for _ in range(steps):
            head = positions[0]
            head[0] += movement[0]
            head[1] += movement[1]
            for i in range(1, len(positions)):
                previous = positions[i - 1]
                current = positions[i]
                if not touching(previous, current):
                    for i in (0, 1):
                        if abs(current[i] - previous[i]) == 1:
                            current[i] = previous[i]
                        elif abs(current[i] - previous[i]) == 2:
                            current[i] = (previous[i] + current[i]) // 2

                visited_spaces.add(tuple(positions[-1]))
    return len(visited_spaces)


def part1(instructions) -> int:
    return simulate_movement(instructions, 2)


def part2(instructions) -> int:
    return simulate_movement(instructions, 10)


print(part1(instructions))
print(part2(instructions))
