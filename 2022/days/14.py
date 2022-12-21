from common import data, mapt, Grid, Point, answer
from typing import Literal

lines = data(
    14,
    sep="\n",
    parser=lambda l: [Point(*mapt(int, part.split(","))) for part in l.split(" -> ")],
)
max_col = max(point.x for line in lines for point in line)
max_row = max(point.y for line in lines for point in line)


def build_board() -> Grid[Literal["#"] | Literal["O"]]:
    board = Grid()
    for line in lines:
        cursor = line[0]
        for position in line[1:]:
            diff = abs(cursor - position) + Point(1, 1)
            x_start = min(cursor.x, position.x)
            y_start = min(cursor.y, position.y)
            for x in range(x_start, x_start + diff.x):
                board[Point(x, y_start)] = "#"
            for y in range(y_start, y_start + diff.y):
                board[Point(x_start, y)] = "#"

            cursor = position
    return board


def part1():
    board = build_board()

    sand_drop = Point(500, 0)
    sand_count = 0
    down = Point(0, 1)
    down_left = Point(-1, 1)
    down_right = Point(1, 1)
    while True:
        sand = sand_drop
        while True:
            if sand.y > max_row:
                return sand_count
            if sand + down not in board:
                sand += down
            elif sand + down_left not in board:
                sand += down_left
            elif sand + down_right not in board:
                sand += down_right
            else:
                board[sand] = "O"
                sand_count += 1
                break


def part2():
    board = build_board()

    sand_drop = Point(500, 0)
    sand_count = 0
    down = Point(0, 1)
    down_left = Point(-1, 1)
    down_right = Point(1, 1)
    while True:
        sand = sand_drop
        while True:
            if sand in board:
                return sand_count
            if (sand + down).y == max_row + 2:
                break
            d = sand + down

            if sand + down not in board:
                sand += down
            elif sand + down_left not in board:
                sand += down_left
            elif sand + down_right not in board:
                sand += down_right
            else:
                break
        board[sand] = "O"
        sand_count += 1


answer(14.1, 683, part1)
answer(14.2, 28821, part2)
