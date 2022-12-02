from common import data

scores = {"X": 1, "Y": 2, "Z": 3}

beats = {"A": "Y", "B": "Z", "C": "X"}
ties = {"A": "X", "B": "Y", "C": "Z"}
loses = {"A": "Z", "B": "X", "C": "Y"}

parts = data(2, sep="\n")
rounds = [part.split(" ") for part in parts]

score = 0
for round in rounds:
    theirs = round[0]
    ours = round[1]
    if beats[theirs] == ours:
        score += 6
    elif ties[theirs] == ours:
        score += 3

    score += scores[ours]

print(score)


score = 0
for round in rounds:
    theirs = round[0]
    outcome = round[1]
    if outcome == "Z":
        score += 6
        score += scores[beats[theirs]]
    elif outcome == "Y":
        score += 3
        score += scores[ties[theirs]]
    else:
        score += scores[loses[theirs]]

print(score)
