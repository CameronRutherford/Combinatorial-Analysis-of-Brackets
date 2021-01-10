import math
import itertools
import copy


# Compute the Conway number C_ab
def c(a, b):
    result = 0
    for i in range(len(a)):
        if a[i:] == (b[:-i] if i != 0 else b):
            result += 2 ** (len(a) - (1 + i))
    return result


# Compute the probability that a beats b
def p(a, b):  # Calculates the probability of pattern a beating pattern b
    if a == b:
        return 0.5
    n = (c(b, b) - c(b, a)) / (c(a, a) - c(a, b))
    return n / (n + 1)


# Input:    list of patterns that represents the seeding (i.e. [HHH, TTT,...])
# Outputs:  dict with the probabilities of each team winning the tournament
def tournament_odds(patterns):
    num_rounds = 1 + int(math.log(len(patterns), 2))

    curr_round = {key: 1.0 for key in patterns}
    next_round = {key: 1.0 for key in patterns}

    for j in range(num_rounds - 1):
        groups = [patterns[i: i + 2 ** j] for i in range(0, len(patterns),\
                                                         2 ** j)]
        pairings = [groups[i: i + 2] for i in range(0, len(groups), 2)]

        for group1, group2 in pairings:
            # Deal with the first group
            for x in group1:
                result = 0
                x_current = curr_round[x]
                for y in group2:
                    result += x_current * curr_round[y] * p(x, y)
                next_round[x] = result
            # Deal with the second group
            for x in group2:
                result = 0
                x_current = curr_round[x]
                for y in group1:
                    result += x_current * curr_round[y] * p(x, y)
                next_round[x] = result

        curr_round = copy.deepcopy(next_round)

    return curr_round


Patterns = [''.join(x) for x in itertools.product('HT', repeat=3)]
Record = {key: [] for key in Patterns}
Winning = {key: 0 for key in Patterns}
for seeding in itertools.permutations(Patterns):
    probabilities = tournament_odds(seeding)
    best_value = 0
    for key, value in probabilities.items():
        Record[key].append(value)

        if value > best_value:
            best_value = value

    for key, value in probabilities.items():
        if value == best_value:
            Winning[key] += 1

for pattern, record in Record.items():
    print("{}: best odds = {:.2f}%, worst odds = {:.2f}%, \
           \"wins\" {} time(s).".format(pattern,\
                                        max(record) * 100,\
                                        min(record) * 100,\
                                        Winning[pattern]))
