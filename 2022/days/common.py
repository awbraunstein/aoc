"""Common Utilities for solving puzzles.

Adapted from Peter Norvig's Advent of Code solutions.
"""

from collections import defaultdict
from itertools import chain
from typing import Iterable
import re
import os


def data(day: int, parser=str, sep="\n") -> list[str]:
    """Read the day's input file into sections separated by `sep`, and apply `parser` to each."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f"../inputs/{day}.txt")
    sections = open(filename).read().rstrip().split(sep)
    return [parser(section) for section in sections]


def quantify(iterable, pred=bool) -> int:
    """Count the number of items in iterable for which pred is true."""
    return sum(1 for item in iterable if pred(item))


def first(iterable, default=None) -> object:
    """Return first item in iterable, or default."""
    return next(iter(iterable), default)


def rest(sequence) -> object:
    return sequence[1:]


def multimap(items: Iterable[tuple]) -> dict:
    "Given (key, val) pairs, return {key: [val, ....], ...}."
    result = defaultdict(list)
    for (key, val) in items:
        result[key].append(val)
    return result


def ints(text: str) -> tuple[int, ...]:
    """Return a tuple of all the integers in text."""
    return tuple(map(int, re.findall("-?[0-9]+", text)))


def atoms(text: str, ignore=r"", sep=None) -> tuple[float | int | str, ...]:
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


def mapt(fn, *args):
    """map(fn, *args) and return the result as a tuple."""
    return tuple(map(fn, *args))


cat = "".join
flatten = chain.from_iterable
