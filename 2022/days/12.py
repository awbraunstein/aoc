from common import data
import heapq

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


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(
    graph: list[list[int]], start: tuple[int, int], goal: tuple[int, int]
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

    open_set: list[tuple[int, tuple[int, int]]] = []
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, goal)}
    heapq.heappush(open_set, (f_score[start], start))

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(graph, current):
            tentative_g_score = g_score[current] + graph[neighbor[0]][neighbor[1]]
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan_distance(
                    neighbor, goal
                )
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def part1() -> int:
    path = a_star(height_map, start, end)
    assert path is not None
    return len(path) - 1


def part2() -> int:
    starts = []
    for r, row in enumerate(height_map):
        for c, v in enumerate(row):
            if v == ord("a"):
                starts.append((r, c))

    paths = [a_star(height_map, start, end) for start in starts]
    return min(len(path) - 1 for path in paths if path is not None)


print(part1())
print(part2())
