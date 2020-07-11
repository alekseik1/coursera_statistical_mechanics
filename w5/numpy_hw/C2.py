import numpy as np
import pylab


def rho_free(x, y, beta):
    return np.exp(-(x - y) ** 2 / (2.0 * beta))


def read_file(filename):
    list_x = []
    list_y = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            list_x.append(float(x))
            list_y.append(float(y))
    f.close()
    return list_x, list_y


def V(x, cubic, quartic):
    return x**2 / 2 + cubic * x**3 + quartic * x**4


beta = 4.0
cubic, quartic = -1., 1.
N = 10
dtau = beta / N
delta = 1.0
n_steps = 1000000
x = [0.0] * N
samples_x = []
k_random = np.random.randint(0, N, n_steps)
x_random = np.random.uniform(-delta, delta, n_steps)
decision_random = np.random.uniform(0, 1, n_steps)
for step in range(n_steps):
    k = k_random[step]
    knext, kprev = (k + 1) % N, (k - 1) % N
    x_new = x[k] + x_random[step]
    old_weight = rho_free(x[knext], x[k], dtau) *\
                 rho_free(x[k], x[kprev], dtau) *\
                 np.exp(-dtau * V(x[k], cubic, quartic))
    # exp(-dtau*V(x)) is a remainder of Trotter decomposition after division
    new_weight = rho_free(x[knext], x_new, dtau) *\
                 rho_free(x_new, x[kprev], dtau) *\
                 np.exp(-dtau * V(x_new, cubic, quartic))
    if decision_random[step] < new_weight / old_weight:
        x[k] = x_new
    if step % 10 == 0:
        samples_x.append(x[0])


pylab.hist(samples_x, normed=True, bins=100, label='QMC')
x, pi_x = read_file('data_anharm_matrixsquaring_beta' + str(beta) + '_quartic' + str(quartic) + '.dat')
pylab.plot(x, pi_x, 'r', label='matrix squaring')
pylab.xlim(-4, 4)
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\pi(x)$')
pylab.title('Harmonic oscillator (matrix squaring vs QMC)')
pylab.savefig('plot_B2_beta%s.png' % beta)
pylab.show()
