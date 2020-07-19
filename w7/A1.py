import math, random, pylab


def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]


def pi_x(x, beta):
    sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return math.exp(-x ** 2 / (2.0 * sigma ** 2)) / math.sqrt(2.0 * math.pi) / sigma


beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
high = low[:]
data = [[] for _ in range(2)]
for step in range(nsteps):
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    data[k].append(low[k])

pylab.hist(data[0], bins=100, density=True, label='particle 1')
pylab.hist(data[1], bins=100, density=True, label='particle 2')
x_data = [i/1000 for i in range(-3000, 3001)]
y_data = [pi_x(x, beta) for x in x_data]
pylab.plot(x_data, y_data, label='analytic solution')
pylab.legend()
pylab.savefig('A1.png')
pylab.show()
pylab.close()
