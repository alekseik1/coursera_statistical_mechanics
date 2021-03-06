import math, random, pylab

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x

beta = 20.0
N = 80
dtau = beta / N
n_steps = 500000
data = []
sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
for step in range(n_steps):
    x_0 = random.gauss(0.0, sigma)
    x = levy_harmonic_path(x_0, x_0, dtau, N)
    k = random.randint(0, N - 1)
    data.append(x[k])

pylab.hist(data, density=True, bins=100, label='QMC')
list_x = [0.1 * a for a in range (-30, 31)]
list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
          math.exp(-xx ** 2 * math.tanh(beta / 2.0)) for xx in list_x]
pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.title('levy_harmonic + sampling x[0] (beta=%s, N=%i)' % (beta, N))
pylab.xlim(-2, 2)
pylab.savefig('plot_B3_beta%s.png' % beta)
pylab.show()