"""Common Utilities for solving puzzles.

Adapted from Peter Norvig's Advent of Code solutions.
"""

from collections import defaultdict
from itertools import chain
from typing import (
    Iterable,
    Sequence,
    TypeVar,
    Callable,
    Optional,
    overload,
    Any,
    Type,
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
def data(day: int, sep: str) -> str:
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
