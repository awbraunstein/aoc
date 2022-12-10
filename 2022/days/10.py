from common import data, cat, mapt

instructions = data(10)


def part1(instructions) -> int:
    X = 1
    cycle = 0
    interesting_signal_strengths = []
    for instruction in instructions:
        if instruction == "noop":
            cycle += 1
            if (cycle + 20) % 40 == 0:
                interesting_signal_strengths.append(cycle * X)
        else:
            cycle += 1
            if (cycle + 20) % 40 == 0:
                interesting_signal_strengths.append(cycle * X)
            cycle += 1
            if (cycle + 20) % 40 == 0:
                interesting_signal_strengths.append(cycle * X)
            X += int(instruction.split(" ")[1])

    return sum(interesting_signal_strengths)


def part2(instructions) -> str:
    crt_size = (40, 6)
    X = 1
    cycle = 0
    crt = []

    def draw_sprite():
        column = cycle % 40
        pixel = "#" if column >= X - 1 and column <= X + 1 else "."
        if column % crt_size[0] == 0:
            crt.append([])
        crt[-1].append(pixel)

    for instruction in instructions:
        if instruction == "noop":
            draw_sprite()
            cycle += 1
        else:
            draw_sprite()
            cycle += 1
            draw_sprite()
            cycle += 1
            X += int(instruction.split(" ")[1])

    return "\n".join(mapt(cat, crt))


print(part1(instructions))
print(part2(instructions))
