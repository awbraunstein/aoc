from common import data, mapt, quantify
from typing import cast

Range = tuple[int, int]
ranges = cast(
    list[tuple[Range, Range]],
    [
        tuple(mapt(int, r.split("-")) for r in line.split(","))
        for line in data(4, sep="\n")
    ],
)


def fully_contained(ranges: tuple[Range, Range]) -> bool:
    a, b = ranges
    return (a[0] <= b[0] and a[1] >= b[1]) or (b[0] <= a[0] and b[1] >= a[1])


print(quantify(ranges, fully_contained))


def overlaps(ranges: tuple[Range, Range]) -> bool:
    a, b = ranges
    return (
        (a[0] >= b[0] and a[0] <= b[1])
        or (a[1] >= b[0] and a[1] <= b[1])
        or (b[0] >= a[0] and b[0] <= a[1])
        or (b[1] >= a[0] and b[1] <= a[1])
    )


print(quantify(ranges, overlaps))
