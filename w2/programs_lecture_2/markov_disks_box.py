import random

def markov(L, n_steps=10**4):
    # L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
    sigma = 0.15
    delta = 0.1
    n_steps = int(n_steps)
    collisions = 0
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
        min_dist = min((b[0] - c[0]) ** 2 + (b[1] - c[1]) ** 2 for c in L if c != a)
        box_cond = min(b[0], b[1]) < sigma or max(b[0], b[1]) > 1.0 - sigma
        if not (box_cond or min_dist < 4.0 * sigma ** 2):
            a[:] = b
        if min_dist < 4.0 * sigma ** 2:
            collisions += 1
    return L, collisions


N_STEPS = 10**6
conf_a = [[0.30, 0.30], [0.30, 0.70], [0.70, 0.30], [0.70,0.70]]
conf_b = [[0.20, 0.20], [0.20, 0.80], [0.75, 0.25], [0.75,0.75]]
conf_c = [[0.30, 0.20], [0.30, 0.80], [0.70, 0.20], [0.70,0.70]]
configurations = [conf_a, conf_b, conf_c]
for config in configurations:
    L, collisions = markov(config, N_STEPS)
    print(collisions)

