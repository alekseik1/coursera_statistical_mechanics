import numpy as np
import pylab


def psi_n_square(x, n):
    if n == -1:
        return 0.0
    else:
        psi = [np.exp(-x ** 2 / 2.0) / np.pi ** 0.25]
        psi.append(np.sqrt(2.0) * x * psi[0])
        for k in range(2, n + 1):
            psi.append(np.sqrt(2.0 / k) * x * psi[k - 1] -
                       np.sqrt((k - 1.0) / k) * psi[k - 2])
        return psi[n] ** 2


def pi_class(x, beta):
    return np.exp(-beta * x ** 2 / 2.0) * np.sqrt(beta / (2.0 * np.pi))


def pi_quant(x, beta):
    return np.exp(-x ** 2 * np.tanh(beta / 2.0)) * np.sqrt(np.tanh(beta / 2.0) / np.pi)


beta = 1.0
nsteps = 500000
delta = 1.0
samples_x = []
x_deltas = np.random.uniform(-delta, delta, nsteps)
n_deltas = np.random.choice([-1, 1], nsteps)
x_choices = np.random.uniform(0, 1, nsteps)
n_choices = np.random.uniform(0, 1, nsteps)
x = 1.0
n = 1
for k in range(nsteps):
    # move 1
    x_new = x + x_deltas[k]
    if x_choices[k] < psi_n_square(x_new, n) / psi_n_square(x, n):
        x = x_new
    # move 2
    n_new = n + n_deltas[k]
    p_acc = np.exp(- beta * n_deltas[k]) * psi_n_square(x, n_new) / psi_n_square(x, n)
    if n_choices[k] < p_acc:
        n = n_new
    # take measures
    if k % 100 == 0:
        samples_x.append(x)


pylab.hist(samples_x, bins=100, normed=True, label='MC')
dx = 0.01
x_data = np.linspace(-3, 3, 10**3)
prob_quant_x = pi_quant(x_data, beta)
prob_class_x = pi_class(x_data, beta)
pylab.plot(x_data, prob_quant_x, label='pi_quant')
pylab.plot(x_data, prob_class_x, label='pi_class')
pylab.xlabel('position $x$')
pylab.ylabel('$\mathrm{prob}(x)$')
pylab.title('harmonic oscillator - beta=%s' % beta)
pylab.legend()
pylab.savefig('plot_A2_beta%s_prob_x.png' % beta)
pylab.show()
