import random


def Q(d):
    dim = d-1
    coords = [0.]*dim
    delta = 0.1
    n_trials = 4000000
    n_hits = 0
    for i in range(n_trials):
        deltas = [random.uniform(-delta, delta) for _ in range(dim)]
        alpha = random.uniform(-1., 1.)
        if sum((coords[i] + deltas[i])**2 for i in range(dim)) < 1.:
            for i in range(dim):
                coords[i] += deltas[i]
        if sum(coords[i]**2 for i in range(dim)) + alpha**2 < 1.:
            n_hits += 1
    return 2.*n_hits/n_trials


print(Q(20))
