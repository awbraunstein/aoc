from common import data, atoms, rest
from collections import defaultdict


def build_data() -> tuple[defaultdict[int, list[str]], list[tuple[int, int, int]]]:
    parts = data(5, sep="\n\n")
    stack_data = list(reversed(parts[0].split("\n")))
    stack_numbers = stack_data[0]
    indices = {i: int(num) for i, num in enumerate(stack_numbers) if num != " "}
    stacks = rest(stack_data)
    boxes = defaultdict(list)
    for row in stacks:
        for i, c in enumerate(row):
            if i in indices and c != " ":
                boxes[indices[i]].append(c)
    instructions = [
        atoms(instruction, ignore=r"[a-zA-Z]") for instruction in parts[1].split("\n")
    ]
    return boxes, instructions


def get_answer(boxes) -> str:
    return "".join([boxes[key][-1] for key in sorted(boxes.keys())])


def part_1() -> str:
    boxes, instructions = build_data()
    for instruction in instructions:
        for i in range(instruction[0]):
            boxes[instruction[2]].append(boxes[instruction[1]].pop())
    return get_answer(boxes)


def part_2() -> str:
    boxes, instructions = build_data()
    for instruction in instructions:
        reorderer = []
        for i in range(instruction[0]):
            reorderer.append(boxes[instruction[1]].pop())
        for e in reversed(reorderer):
            boxes[instruction[2]].append(e)
    return get_answer(boxes)


print(part_1())
print(part_2())
