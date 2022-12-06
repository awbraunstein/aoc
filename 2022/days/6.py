from common import data
from collections import Counter

signal = data(6)[0]


def unique_window(signal: str, window_size: int) -> int:
    window: Counter[str] = Counter()
    for i in range(window_size):
        window[signal[i]] += 1
    idx = window_size
    while idx < len(signal):
        if len(window) == window_size:
            return idx
        to_remove = signal[idx - window_size]
        window[to_remove] -= 1
        if window[to_remove] == 0:
            del window[to_remove]
        window[signal[idx]] += 1
        idx += 1

    raise Exception()


def part1(signal: str) -> int:
    return unique_window(signal, 4)


def part2(signal: str) -> int:
    return unique_window(signal, 14)


print(part1(signal))
print(part2(signal))
