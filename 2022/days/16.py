from common import data, atoms, answer
from itertools import combinations
import re


def parser(line: str):
    matches = re.findall(
        r"Valve (\w\w) has flow rate=(\d*); tunnels? leads? to valves? (.*)", line
    )[0]
    assert len(matches) == 3, str(matches)
    return matches[0], int(matches[1]), atoms(matches[2], ignore=" ", sep=",")


lines = data(16, sep="\n", parser=parser)


graph = {}
valve_to_mask = {}
flow_rates = {}
for i, line in enumerate(lines):
    graph[line[0]] = line[2]
    flow_rates[line[0]] = line[1]
    valve_to_mask[line[0]] = 1 << i


def get_paths(
    time_remaining: int, start: str
) -> list[tuple[int, list[tuple[int, str]]]]:
    opened_valves = set([valve for valve, flow in flow_rates.items() if flow == 0])
    known_states: set[tuple[str, int, int]] = set()
    all_paths: list[tuple[int, list[tuple[int, str]]]] = []

    def explore(valve, time_remaining, total_pressure, path: list):
        key = (valve, time_remaining, total_pressure)
        if key in known_states:
            all_paths.append((total_pressure, list(path)))
            return
        known_states.add(key)
        if time_remaining == 0 or len(opened_valves) == len(graph):
            all_paths.append((total_pressure, list(path)))
            return
        # Options:
        # 1. Open the valve (if closed),
        # 2. Travel to a neighbor
        # Return the max pressure of any of these options.
        new_time = time_remaining - 1
        if valve not in opened_valves:
            flow = new_time * flow_rates[valve]
            opened_valves.add(valve)
            path.append((1, valve))
            explore(valve, new_time, total_pressure + flow, path)
            path.pop()
            opened_valves.remove(valve)

        for neighbor in graph[valve]:
            path.append((0, neighbor))
            explore(neighbor, new_time, total_pressure, path)
            path.pop()

    explore(start, time_remaining, 0, [])

    return all_paths


def part1() -> int:
    return max(value[0] for value in get_paths(30, "AA"))


def part2() -> int:
    paths = get_paths(26, "AA")
    paths_by_opened_set: dict[int, tuple[int, list[tuple[int, str]]]] = {}
    possible_valves: set[int] = set()
    for path in paths:
        key = 0
        for segment in path[1]:
            if segment[0] == 1:
                key |= valve_to_mask[segment[1]]
                possible_valves.add(valve_to_mask[segment[1]])

        if key not in paths_by_opened_set or path[0] > paths_by_opened_set[key][0]:
            paths_by_opened_set[key] = path

    return max(
        paths_by_opened_set[a][0] + paths_by_opened_set[b][0]
        for a, b in combinations(paths_by_opened_set.keys(), 2)
        if a & b == 0
    )


answer(16.1, 1741, part1)
answer(16.2, 2316, part2)
