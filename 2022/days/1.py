from common import data

elves = data(1, sep="\n\n")

calories_per_elf = [sum(map(int, elf.split("\n"))) for elf in elves]

print(max(calories_per_elf))
print(sum(sorted(calories_per_elf, reverse=True)[:3]))
