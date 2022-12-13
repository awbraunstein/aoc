from common import data
from collections import deque

height_map_strings = data(12, sep="\n", parser=list)

height_map: list[list[int]] = []
start: tuple[int, int] = (0, 0)
end: tuple[int, int] = (0, 0)

for r, row in enumerate(height_map_strings):
    height_map.append([])
    for c, v in enumerate(row):
        if v == "S":
            start = (r, c)
            v = "a"
        elif v == "E":
            end = (r, c)
            v = "z"
        val = ord(v)
        height_map[r].append(val)


def search(
    graph: list[list[int]], starts: list[tuple[int, int]], goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    def get_neighbors(
        graph: list[list[int]], current: tuple[int, int]
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        for possible in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            r, c = (current[0] + possible[0], current[1] + possible[1])
            if r >= 0 and r < len(graph) and c >= 0 and c < len(graph[r]):
                current_height = graph[current[0]][current[1]]
                target_height = graph[r][c]
                if (
                    not target_height > current_height
                    or target_height - current_height == 1
                ):
                    neighbors.append((r, c))
        return neighbors

    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return list(reversed(total_path))

    queue = deque(starts)
    seen: set[tuple[int, int]] = set(starts)
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(came_from, current)
        neighbors = get_neighbors(graph, current)
        for neighbor in neighbors:
            if neighbor not in seen:
                seen.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return None


def part1() -> int:
    path = search(height_map, [start], end)
    assert path is not None
    return len(path) - 1


def part2() -> int:
    starts = []
    for r, row in enumerate(height_map):
        for c, v in enumerate(row):
            if v == ord("a"):
                starts.append((r, c))
    path = search(height_map, starts, end)
    assert path is not None
    return len(path) - 1


print(part1())
print(part2())
