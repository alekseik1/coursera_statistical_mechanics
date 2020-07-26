import math, random, pylab


def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]


def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)


y_data1, y_data2 = [], []
x_data = [i/10. for i in range(1, 60, 3)]
for beta in x_data:
    nsteps = 50000
    low = levy_harmonic_path(2)
    high = low[:]
    data = []
    total_ones, total_twos = 0, 0
    for step in range(nsteps):
        # move 1
        if low[0] == high[0]:
            k = random.choice([0, 1])
            low[k] = levy_harmonic_path(1)[0]
            high[k] = low[k]
            total_ones += 1
        else:
            low[0], low[1] = levy_harmonic_path(2)
            high[1] = low[0]
            high[0] = low[1]
            total_twos += 1
        data += low[:]
        # move 2
        weight_old = (rho_harm_1d(low[0], high[0], beta) *
                      rho_harm_1d(low[1], high[1], beta))
        weight_new = (rho_harm_1d(low[0], high[1], beta) *
                      rho_harm_1d(low[1], high[0], beta))
        if random.uniform(0.0, 1.0) < weight_new / weight_old:
            high[0], high[1] = high[1], high[0]
    y_data1.append(total_ones/float(total_ones + total_twos))
    y_data2.append(total_twos/float(total_ones + total_twos))

pylab.scatter(x_data, y_data1, label='QMC one cycle')
pylab.scatter(x_data, y_data2, label='QMC two cycles')

# Analytical
def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))

fract_two_cycles = [z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta)) for beta in x_data]
fract_one_cycle = [z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta)) for beta in x_data]

pylab.plot(x_data, fract_one_cycle, label='analytical one cycle')
pylab.plot(x_data, fract_two_cycles, label='analytical two cycles')

pylab.legend()
pylab.xlabel('beta')
pylab.xlim(0., 6.)
pylab.ylabel('probability')
pylab.ylim(0., 1.)
pylab.savefig('A2_cont.png')
pylab.show()
pylab.close()
