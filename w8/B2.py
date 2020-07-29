import random
import math
import os
import pylab


def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E



def get_configuration(filename):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        S = []
        for line in f:
            S.append(int(line))
        f.close()
        print('Starting from file', filename)
    else:
        S = [random.choice([1, -1]) for k in range(N)]
        print('Starting from a random configuration')
    return S


def write_configuration(filename, S):
    f = open(filename, 'w')
    for a in S:
        f.write(str(a) + '\n')
    f.close()


def get_cv(L, temperature):
    p = 1.0 - math.exp(-2.0 / temperature)
    filename = 'data_wolf_' + str(L) + '_' + str(temperature) + '.txt'
    S = get_configuration(filename)
    E = [energy(S, N, nbr)]
    for step in range(nsteps):
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            #j = random.choice(Pocket)
            j = Pocket.pop()
            for l in nbr[j]:
                # Equal spins
                if S[l] == S[j] and l not in Cluster \
                       and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
            #Pocket.remove(j)
        for j in Cluster:
            S[j] *= -1
        E.append(energy(S, N, nbr))
    write_configuration(filename, S)

    E_mean = sum(E) / len(E)
    E2_mean = sum(a ** 2 for a in E) / len(E)
    cv = (E2_mean - E_mean ** 2) / N / temperature ** 2
    return cv


for L in [2, 4, 8,]: #16, 32, 64]:
    N = L * L
    nbr = {i: ((i // L) * L + (i + 1) % L, (i + L) % N,
               (i // L) * L + (i - 1) % L, (i - L) % N)
           for i in range(N)}
    #T = 2.27
    nsteps = 100000

    x_data = [x/20. for x in range(10, 81)]
    y_data = []
    for T in x_data:
        y_data.append(get_cv(L, T))
    pylab.plot(x_data, y_data, label='L={}'.format(L))

pylab.savefig('B2.png')
pylab.show()
pylab.close()
