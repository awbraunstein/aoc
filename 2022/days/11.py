from functools import reduce
from common import data, cat, mapt, atoms
from typing import Callable
from collections import deque
from operator import mul, add
from dataclasses import dataclass


@dataclass
class Monkey:
    id: int
    items: deque[int]
    operation: Callable[[int], int]
    test_divisible_by: int
    test_true: int
    test_false: int

    inspect_count: int = 0

    def turn(
        self, monkeys: list["Monkey"], relief: bool = True, field: int | None = None
    ):
        while self.items:
            item = self.items.popleft()
            self.inspect_count += 1
            item = self.operation(item)
            if relief:
                item //= 3
            if field is not None:
                item %= field
            target = (
                self.test_true
                if item % self.test_divisible_by == 0
                else self.test_false
            )
            monkeys[target].items.append(item)

    @classmethod
    def from_string(cls, data: str) -> "Monkey":
        lines = data.split("\n")
        id = atoms(lines[0], ignore=":")[1]
        items = deque(atoms(lines[1], ignore="[:,a-zA-Z]"))

        def make_operation(line: str) -> Callable[[int], int]:
            parts = atoms(line)
            op = add if parts[4] == "+" else mul

            def fn(old: int) -> int:
                left = old if parts[3] == "old" else parts[3]
                right = old if parts[5] == "old" else parts[5]
                return op(left, right)

            return fn

        operation = make_operation(lines[2])

        test_divisible_by = atoms(lines[3])[-1]
        test_true = atoms(lines[4])[-1]
        test_false = atoms(lines[5])[-1]
        return Monkey(
            id=id,
            items=items,
            operation=operation,
            test_divisible_by=test_divisible_by,
            test_true=test_true,
            test_false=test_false,
        )


def part1() -> int:
    monkeys: list[Monkey] = data(11, sep="\n\n", parser=Monkey.from_string)
    field = reduce(mul, [monkey.test_divisible_by for monkey in monkeys], 1)
    for _ in range(20):
        for monkey in monkeys:
            monkey.turn(monkeys, field=field)
    most_active_monkeys = sorted(
        [monkey.inspect_count for monkey in monkeys], reverse=True
    )
    return reduce(mul, most_active_monkeys[:2], 1)


def part2() -> int:
    monkeys: list[Monkey] = data(11, sep="\n\n", parser=Monkey.from_string)
    field = reduce(mul, [monkey.test_divisible_by for monkey in monkeys], 1)
    for _ in range(10000):
        for monkey in monkeys:
            monkey.turn(monkeys, relief=False, field=field)
    most_active_monkeys = sorted(
        [monkey.inspect_count for monkey in monkeys], reverse=True
    )
    return reduce(mul, most_active_monkeys[:2], 1)


print(part1())
print(part2())
