from common import data, mapt
from functools import cmp_to_key


def compare(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        if left > right:
            return 1
        return 0
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i])
            if result != 0:
                return result
        if len(left) < len(right):
            return -1
        if len(left) > len(right):
            return 1
        return 0
    if isinstance(left, int):
        return compare([left], right)
    if isinstance(right, int):
        return compare(left, [right])
    return 0


def part1() -> int:
    packet_pairs = data(
        13, sep="\n\n", parser=lambda pair: mapt(eval, pair.split("\n"))
    )

    correct_index_sum = 0
    for i, (left, right) in enumerate(packet_pairs):
        result = compare(left, right)
        if result == -1:
            correct_index_sum += i + 1
    return correct_index_sum


def part2() -> int:
    divider_packets = [[[2]], [[6]]]
    packets = [
        packet
        for packet in data(13, sep="\n", parser=lambda l: eval(l) if l != "" else None)
        if packet is not None
    ] + divider_packets
    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    signal = 1
    for i, packet in enumerate(sorted_packets):
        if packet in divider_packets:
            signal *= i + 1
    return signal


print(part1())
print(part2())
