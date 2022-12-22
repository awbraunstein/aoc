from common import data, mapt, Grid, Point, answer, ints, manhattan_distance, rest
from typing import Literal


def parse_line(line: str) -> tuple[Point, Point]:
    nums = ints(line)
    assert len(nums) == 4
    sensor = Point(nums[0], nums[1])
    beacon = Point(nums[2], nums[3])
    return sensor, beacon, manhattan_distance(sensor, beacon)


lines = data(15, sep="\n", parser=parse_line)


def invalid_spots_for_y(
    beacons: list[tuple[Point, Point, int]], target_row, search_range=None
) -> tuple[int, list[tuple[int, int]], set[int]]:
    ranges = []
    invalid_spots: set[int] = set()
    for sensor, beacon, distance in beacons:
        if sensor.y == target_row:
            invalid_spots.add(sensor.x)
        if beacon.y == target_row:
            invalid_spots.add(beacon.x)
        remaining_distance = distance - abs(sensor.y - target_row)
        if remaining_distance >= 0:
            ranges.append(
                (sensor.x - remaining_distance, sensor.x + remaining_distance)
            )

    if len(ranges) == 0:
        return 0, [], set()

    ranges = sorted(ranges)

    merged_ranges: list[tuple[int, int]] = []
    for current in ranges:
        if search_range is not None:
            if current[1] < search_range[0] or current[0] > search_range[1]:
                continue
            if current[0] < search_range[0]:
                current = (search_range[0], current[1])
            elif current[1] > search_range[1]:
                current = (current[0], search_range[1])
        if len(merged_ranges) == 0:
            merged_ranges.append(current)
            continue
        prev = merged_ranges[-1]
        if current[0] <= prev[1]:
            merged_ranges[-1] = (prev[0], max(current[1], prev[1]))
        else:
            merged_ranges.append(current)

    count = 0
    for start, end in merged_ranges:
        count += (end - start) + 1

    return (count - len(invalid_spots), merged_ranges, invalid_spots)


def part1() -> int:
    count, _, _ = invalid_spots_for_y(lines, 2000000)
    return count


def part2():
    max_xy = 4000000
    total_spots = max_xy + 1
    for i in range(max_xy + 1):
        invalid_spots, ranges, used_xs = invalid_spots_for_y(lines, i, (0, max_xy))
        if total_spots - (invalid_spots + len(used_xs)):
            if len(ranges) == 1:
                if ranges[0][0] != 0:
                    return i
                if ranges[0][1] != max_xy:
                    return (max_xy * 4000000) + i

            assert len(ranges) == 2
            return ((ranges[0][1] + 1) * 4000000) + i


answer(15.1, 6124805, part1)
answer(15.2, 12555527364986, part2)
