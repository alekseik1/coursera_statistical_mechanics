import pylab
import numpy as np


def psi_0_sq(x):
    return 1/np.sqrt(np.pi)*np.exp(-x**2)


delta = 0.5
n_runs = 10**6
x = np.zeros(n_runs)
deltas = np.random.uniform(-delta, delta, n_runs)
for k in range(n_runs-1):
    x[k] = x[k-1]
    d = deltas[k]
    if (np.random.uniform(0, 1) < psi_0_sq(x[k]+d)/psi_0_sq(x[k])).all():
        x[k] += d
hist_data = x


pylab.hist(hist_data, bins=100, density=True, label='histgram')
x_data = np.linspace(-3, 3, 10**3)
y_data = psi_0_sq(x_data)
pylab.plot(x_data, y_data, label='analytical')
pylab.xlabel('x')
pylab.ylabel(r'$\psi^2$')
pylab.title(r'$\psi^2$ histogram and curve')
pylab.legend()
pylab.savefig('A1.png')
pylab.show()
pylab.close()
