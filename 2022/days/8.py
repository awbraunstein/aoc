from common import data, mapt

grid = data(8, parser=lambda x: mapt(int, list(x)))


def part1(grid: list[list[int]]) -> int:
    # left, right, top, bottom
    max_heights: list[list[list[int]]] = []
    for r in range(len(grid)):
        max_heights.append([])
        for c in range(len(grid[r])):
            max_heights[r].append([-1, -1, -1, -1])

    # From the left
    for r in range(len(grid)):
        max_height = -1
        for c in range(len(grid[r])):
            max_heights[r][c][0] = max_height
            max_height = max(max_height, grid[r][c])

    # From the right
    for r in range(len(grid)):
        max_height = -1
        for c in reversed(range(len(grid[r]))):
            max_heights[r][c][1] = max_height
            max_height = max(max_height, grid[r][c])

    # From the top
    for c in range(len(grid[0])):
        max_height = -1
        for r in range(len(grid)):
            max_heights[r][c][2] = max_height
            max_height = max(max_height, grid[r][c])

    # From the bottom
    for c in range(len(grid[0])):
        max_height = -1
        for r in reversed(range(len(grid))):
            max_heights[r][c][3] = max_height
            max_height = max(max_height, grid[r][c])

    visible_trees = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            height = grid[r][c]
            if any([height > max_height for max_height in max_heights[r][c]]):
                visible_trees += 1
    return visible_trees


def part2(grid: list[list[int]]) -> int:
    def scenic_score(grid, r, c) -> int:
        height = grid[r][c]
        score = 1

        visible_trees = 0
        next_c = c - 1
        while next_c >= 0 and grid[r][next_c] < height:
            visible_trees += 1
            next_c -= 1
        if next_c > 0:
            visible_trees += 1
        score *= visible_trees

        visible_trees = 0
        next_r = r + 1
        while next_r < len(grid) and grid[next_r][c] < height:
            visible_trees += 1
            next_r += 1
        if next_r < len(grid):
            visible_trees += 1
        score *= visible_trees

        visible_trees = 0
        next_r = r - 1
        while next_r >= 0 and grid[next_r][c] < height:
            visible_trees += 1
            next_r -= 1
        if next_r > 0:
            visible_trees += 1
        score *= visible_trees
        return score

    max_score = 0
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            max_score = max(max_score, scenic_score(grid, r, c))

    return max_score


print(part1(grid))
print(part2(grid))
