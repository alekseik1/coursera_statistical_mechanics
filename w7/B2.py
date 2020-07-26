import random, math, pylab

def levy_harmonic_path_3d(k):
    x0 = tuple([random.gauss(0.0, 1.0 / math.sqrt(2.0 *
                math.tanh(k * beta / 2.0))) for d in range(3)])
    x = [x0]
    for j in range(1, k):
        Upsilon_1 = 1.0 / math.tanh(beta) + 1.0 / \
                          math.tanh((k - j) * beta)
        Upsilon_2 = [x[j - 1][d] / math.sinh(beta) + x[0][d] /
                     math.sinh((k - j) * beta) for d in range(3)]
        x_mean = [Upsilon_2[d] / Upsilon_1 for d in range(3)]
        sigma = 1.0 / math.sqrt(Upsilon_1)
        dummy = [random.gauss(x_mean[d], sigma) for d in range(3)]
        x.append(tuple(dummy))
    return x

def rho_harm_3d(x, xp):
    Upsilon_1 = sum((x[d] + xp[d]) ** 2 / 4.0 *
                    math.tanh(beta / 2.0) for d in range(3))
    Upsilon_2 = sum((x[d] - xp[d]) ** 2 / 4.0 /
                    math.tanh(beta / 2.0) for d in range(3))
    return math.exp(- Upsilon_1 - Upsilon_2)

N = 512
T_star = 0.4
beta = 1.0 / (T_star * N ** (1.0 / 3.0))
data_all, data_long = [], []
k_min = 10
positions = {}
# Initial condition
for k in range(N):
    a = levy_harmonic_path_3d(1)
    positions[a[0]] = a[0]
# Monte Carlo loop
nsteps = 100000
for step in range(nsteps):
    # move 1: resample one permutation cycle
    boson_a = random.choice(list(positions.keys()))
    perm_cycle = []
    while True:
        perm_cycle.append(boson_a)
        boson_b = positions.pop(boson_a)
        if boson_b == perm_cycle[0]:
            break
        else:
           boson_a = boson_b
    k = len(perm_cycle)
    data_all.append(boson_a[0])
    if k > k_min:
        data_long.append(boson_a[0])
    perm_cycle = levy_harmonic_path_3d(k)
    positions[perm_cycle[-1]] = perm_cycle[0]
    for k in range(len(perm_cycle) - 1):
        positions[perm_cycle[k]] = perm_cycle[k + 1]
    # move 2: exchange
    a_1 = random.choice(list(positions.keys()))
    b_1 = positions.pop(a_1)
    a_2 = random.choice(list(positions.keys()))
    b_2 = positions.pop(a_2)
    weight_new = rho_harm_3d(a_1, b_2) * rho_harm_3d(a_2, b_1)
    weight_old = rho_harm_3d(a_1, b_1) * rho_harm_3d(a_2, b_2)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        positions[a_1] = b_2
        positions[a_2] = b_1
    else:
        positions[a_1] = b_1
        positions[a_2] = b_2


pylab.hist(data_all, normed=True, alpha=0.5, bins=100, label='all data')
pylab.hist(data_long, normed=True, alpha=0.5, bins=100, label='long data')
# Analytical
def psi0_sq(x):
    return math.exp(-x**2)/math.sqrt(math.pi)

x_data = [i/10. for i in range(-30, 31)]
y_data = [psi0_sq(x) for x in x_data]
pylab.plot(x_data, y_data, label='analytical psi^2(x)')
pylab.xlim(-3, 3)
pylab.legend()
pylab.savefig('B2.png')
pylab.show()
pylab.close()
