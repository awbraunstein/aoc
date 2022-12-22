"""Common Utilities for solving puzzles.

Adapted from Peter Norvig's Advent of Code solutions.
"""

import time
from collections import defaultdict, abc
from itertools import chain
from typing import (
    Iterable,
    Mapping,
    NamedTuple,
    Sequence,
    TypeVar,
    Callable,
    Generic,
    Optional,
    overload,
    ParamSpec,
)
import re
import os


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
P = ParamSpec("P")


@overload
def data(day: int) -> str:
    ...


@overload
def data(day: int, sep: str) -> list[str]:
    ...


@overload
def data(day: int, parser: Callable[[str], T], sep: str) -> T:
    ...


@overload
def data(day: int, parser: Callable[[str], T]) -> T:
    ...


def data(day, parser=str, sep="\n"):
    """Read the day's input file into sections separated by `sep`, and apply `parser` to each."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"../inputs/{day}.txt")
    sections = open(filename).read().rstrip().split(sep)
    return [parser(section) for section in sections]


def quantify(iterable: Iterable[T], pred: Callable[[T], bool] = bool) -> int:
    """Count the number of items in iterable for which pred is true."""
    return sum(1 for item in iterable if pred(item))


def first(iterable: Iterable[T], default: Optional[V] = None) -> T | Optional[V]:
    """Return first item in iterable, or default."""
    return next(iter(iterable), default)


def rest(sequence: Sequence[T]) -> Sequence[T]:
    return sequence[1:]


def multimap(items: Iterable[tuple[K, V]]) -> dict[K, list[V]]:
    "Given (key, val) pairs, return {key: [val, ....], ...}."
    result = defaultdict(list)
    for (key, val) in items:
        result[key].append(val)
    return result


def ints(text: str) -> tuple[int, ...]:
    """Return a tuple of all the integers in text."""
    return tuple(map(int, re.findall("-?[0-9]+", text)))


def atoms(
    text: str, ignore: str = r"", sep: Optional[str] = None
) -> tuple[float | int | str, ...]:
    """Parse text into atoms (numbers or strs), possibly ignoring a regex."""
    if ignore:
        text = re.sub(ignore, "", text)
    return tuple(map(atom, text.split(sep)))


def atom(text: str) -> float | int | str:
    """Parse text into a single float or int or str."""
    try:
        val = float(text)
        return round(val) if round(val) == val else val
    except ValueError:
        return text


def dotproduct(A, B) -> float:
    return sum(a * b for a, b in zip(A, B))


def mapt(fn: Callable[[K], T], iter: Iterable[K]) -> tuple[T, ...]:
    """map(fn, *args) and return the result as a tuple."""
    return tuple(map(fn, iter))


cat = "".join
flatten = chain.from_iterable


def answer(puzzle: float, correct: T, code: Callable[[], T]) -> None:
    start = time.perf_counter()
    got = code()
    secs = time.perf_counter() - start
    msg = f"{secs:5.3f} seconds for " + (
        f"correct answer: {got}"
        if (got == correct)
        else f"WRONG!! ANSWER: {got}; EXPECTED {correct}"
    )
    print(msg)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __abs__(self) -> "Point":
        return Point(abs(self.x), abs(self.y))


def distance(p1: Point, p2: Point) -> float:
    diff = p2 - p1
    return (diff.x**2 + diff.y**2) ** 0.5


def manhattan_distance(p1: Point, p2: Point) -> int:
    diff = abs(p2 - p1)
    return diff.x + diff.y


Directions = tuple[Point, ...]

directions4 = North, South, East, West = (
    Point(0, 1),
    Point(0, -1),
    Point(1, 0),
    Point(-1, 0),
)
directions8 = directions4 + (Point(-1, -1), Point(-1, 1), Point(1, -1), Point(1, 1))


class Grid(Generic[T], dict[Point, T]):
    def __init__(
        self,
        mapping_or_rows: Mapping[Point, T] | Iterable[Iterable[T]] = (),
        directions: Directions = directions4,
    ):
        self.directions = directions
        self.update(
            mapping_or_rows  # type: ignore
            if isinstance(mapping_or_rows, abc.Mapping)
            else {
                Point(x, y): v
                for y, row in enumerate(mapping_or_rows)
                for x, v in enumerate(row)
            }
        )

    def copy(self) -> "Grid[T]":
        return Grid(self, self.directions)

    def neighbors(self, p: Point) -> list[Point]:
        return [p + delta for delta in self.directions if p in self]

    def to_rows(
        self,
        default: V | None = None,
        xs: Sequence[int] | None = None,
        ys: Sequence[int] | None = None,
    ) -> list[list[T | V | None]]:
        xs = xs or range(max(p.x for p in self) + 1)
        ys = ys or range(max(p.y for p in self) + 1)
        return [[self.get(Point(x, y), default) for x in xs] for y in ys]

    def draw_picture(
        self,
        sep: str = "",
        default: str = ".",
        xs: Sequence[int] | None = None,
        ys: Sequence[int] | None = None,
    ) -> str:
        return "\n".join(
            [
                sep.join(map(str, row))
                for row in self.to_rows(default=default, xs=xs, ys=ys)
            ]
        )
