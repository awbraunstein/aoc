from common import data

terminal_output = data(7)

working_directory: list[str] = []

file_system: dict[str, dict | int] = {}

i = 0
while i < len(terminal_output):
    line = terminal_output[i]
    if line.startswith("$"):
        command = line[2:]
        if command.startswith("cd "):
            arg = command.split(" ")[1]
            if arg == "/":
                working_directory = []
            elif arg == "..":
                working_directory.pop()
            else:
                working_directory.append(arg)
            i += 1
        elif command == "ls":
            j = 1
            sub_dirs = []
            files = []
            while i + j < len(terminal_output) and not terminal_output[
                i + j
            ].startswith("$"):
                output = terminal_output[i + j].split(" ")
                if output[0] == "dir":
                    sub_dirs.append(output[1])
                else:
                    files.append((output[1], int(output[0])))
                j += 1
            current_dir = file_system
            for dir in working_directory:
                current_dir = current_dir[dir]
            for sub_dir in sub_dirs:
                if sub_dir not in current_dir:
                    current_dir[sub_dir] = {}
            for file in files:
                current_dir[file[0]] = file[1]
            i += j
        else:
            raise Exception("Unrecognized command")
    else:
        raise Exception("We should only see commands")


def dir_sizes(file_system) -> list[int]:

    dir_sizes: list[int] = []

    def dfs(directory, dir_sizes) -> int:
        dir_size = 0
        for name, dir_or_size in directory.items():
            if type(dir_or_size) == int:
                dir_size += dir_or_size
            else:
                dir_size += dfs(dir_or_size, dir_sizes)

        dir_sizes.append(dir_size)
        return dir_size

    dfs(file_system, dir_sizes)

    return dir_sizes


def part1(file_system) -> int:
    return sum(dir for dir in dir_sizes(file_system) if dir <= 100000)


def part2(file_system) -> int:
    total_disk_space = 70000000
    min_free_disk_space = 30000000

    sizes = dir_sizes(file_system)
    total_used_disk_space = max(sizes)
    free_disk_space = total_disk_space - total_used_disk_space
    return min(size for size in sizes if size + free_disk_space >= min_free_disk_space)


print(part1(file_system))
print(part2(file_system))
