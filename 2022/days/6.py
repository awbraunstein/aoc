from common import data

signal = data(6)[0]


def unique_window(signal: str, window_size: int) -> int:
    for i in range(len(signal) - window_size):
        if len(set(signal[i : i + window_size])) == window_size:
            return i + window_size

    raise Exception


def part1(signal: str) -> int:
    return unique_window(signal, 4)


def part2(signal: str) -> int:
    return unique_window(signal, 14)


print(part1(signal))
print(part2(signal))
