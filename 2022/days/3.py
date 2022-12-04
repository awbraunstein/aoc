import functools
from common import data

sacks = data(3, sep="\n")
sacks_with_compartments: list[tuple[str, str]] = []
for s in sacks:
    sacks_with_compartments.append((s[: len(s) // 2], s[len(s) // 2 :]))

overlapping_items: list[str] = []
for sack in sacks_with_compartments:
    overlapping_items.append(set(sack[0]).intersection(set(sack[1])).pop())


def priority(item_type: str) -> int:
    assert len(item_type) == 1
    item_type_ord = ord(item_type)
    if item_type_ord >= ord("a") and item_type_ord <= ord("z"):
        return (item_type_ord - ord("a")) + 1
    else:
        return (item_type_ord - ord("A")) + 27


print(sum(map(priority, overlapping_items)))

total = 0
i = 0
while i < len(sacks):
    group = []
    for j in range(3):
        group.append(set(sacks[i]))
        i += 1
    total += priority(functools.reduce(lambda s1, s2: s1.intersection(s2), group).pop())

print(total)
