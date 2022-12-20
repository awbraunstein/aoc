from common import data, mapt

lines = data(
    14,
    sep="\n",
    parser=lambda l: [mapt(int, part.split(",")) for part in l.split(" -> ")],
)
max_col = max(c for line in lines for (c, r) in line)
max_row = max(r for line in lines for (c, r) in line)

board = [["." for _ in range(max_col + 1)] for _ in range(max_row + 1)]

for line in lines:
    cursor = line[0]
    for position in line[1:]:
        cursor_c, cursor_r = cursor
        position_c, position_r = position
        c_diff = abs(cursor_c - position_c) + 1
        r_diff = abs(cursor_r - position_r) + 1
        c_start = min(cursor_c, position_c)
        r_start = min(cursor_r, position_r)
        for c in range(c_start, c_start + c_diff):
            board[r_start][c] = "#"
        for r in range(r_start, r_start + r_diff):
            board[r][c_start] = "#"

        cursor = position


def print_board(board):
    print("\n".join(" ".join(line) for line in board))


def part1():
    board = [["." for _ in range(max_col + 2)] for _ in range(max_row + 2)]

    for line in lines:
        cursor = line[0]
        for position in line[1:]:
            cursor_c, cursor_r = cursor
            position_c, position_r = position
            c_diff = abs(cursor_c - position_c) + 1
            r_diff = abs(cursor_r - position_r) + 1
            c_start = min(cursor_c, position_c)
            r_start = min(cursor_r, position_r)
            for c in range(c_start, c_start + c_diff):
                board[r_start][c] = "#"
            for r in range(r_start, r_start + r_diff):
                board[r][c_start] = "#"

            cursor = position

    sand_drop = (500, 0)
    sand_count = 0
    while True:
        sand_c, sand_r = sand_drop
        while True:
            next_r = sand_r + 1
            if sand_r > max_row:
                return sand_count
            if board[next_r][sand_c] == ".":
                sand_r = next_r
            elif board[next_r][sand_c - 1] == ".":
                sand_r = next_r
                sand_c = sand_c - 1
            elif board[next_r][sand_c + 1] == ".":
                sand_r = next_r
                sand_c = sand_c + 1
            else:
                board[sand_r][sand_c] = "O"
                sand_count += 1
                break


def part2():
    board = [["." for _ in range(max_col + 200)] for _ in range((max_row + 2) + 1)]

    for line in lines:
        cursor = line[0]
        for position in line[1:]:
            cursor_c, cursor_r = cursor
            position_c, position_r = position
            c_diff = abs(cursor_c - position_c) + 1
            r_diff = abs(cursor_r - position_r) + 1
            c_start = min(cursor_c, position_c)
            r_start = min(cursor_r, position_r)
            for c in range(c_start, c_start + c_diff):
                board[r_start][c] = "#"
            for r in range(r_start, r_start + r_diff):
                board[r][c_start] = "#"

            cursor = position

    sand_drop = (500, 0)
    sand_count = 0
    while True:
        sand_c, sand_r = sand_drop
        if board[sand_r][sand_c] != ".":
            return sand_count
        while True:
            next_r = sand_r + 1
            if next_r == max_row + 2:
                break
            elif board[next_r][sand_c] == ".":
                sand_r = next_r
            elif board[next_r][sand_c - 1] == ".":
                sand_r = next_r
                sand_c = sand_c - 1
            elif board[next_r][sand_c + 1] == ".":
                sand_r = next_r
                sand_c = sand_c + 1
            else:
                break
        board[sand_r][sand_c] = "O"
        sand_count += 1


print(part1())
print(part2())
