import random
import math


def Q(d):
    dim = d-1
    coords = [0.]*dim
    delta = 0.1
    n_trials = 400000
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


def V_sph(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)


for d in range(1, 20):
    print('dim:', d,
          'expected:', V_sph(d),
          'actual', Q(d),
          'divergence:', (V_sph(d) - Q(d))/V_sph(d)
          )
