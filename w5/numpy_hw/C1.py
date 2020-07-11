import numpy as np
import pylab


def rho_free(x, xp, beta):
    return np.exp(-(x - xp) ** 2 / (2.0 * beta))/np.sqrt(2.0 * np.pi * beta)


def V(x, cubic, quartic):
    pot = x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4
    return pot


def rho_anharmonic_trotter(grid, beta, cubic, quartic):
    xx, pp = np.meshgrid(grid, grid)
    return rho_free(xx, pp, beta) * np.exp(-0.5*beta * (V(xx, cubic, quartic) + V(pp, cubic, quartic)))


quartic = 1.
cubic = - quartic
x_max = 8
dx = 10**-2
x = np.arange(-x_max, x_max+dx, dx)
beta_tmp = 2.0 ** (-6)
beta = 2.0 ** 2
rho = rho_anharmonic_trotter(x, beta_tmp, cubic, quartic)
while beta_tmp < beta:
    rho = np.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0
    print('beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp))

Z = dx*np.trace(rho)
pi_of_x = np.diag(rho)/Z
f = open('data_anharm_matrixsquaring_beta' + str(beta) + '_quartic' + str(quartic) + '.dat', 'w')
for j in range(len(x)):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

pylab.plot(x, pi_of_x)
pylab.xlim(-2, 2)
pylab.xlabel('$x$')
pylab.ylabel('$\pi(x)$')
pylab.title('Matrix-squaring for anharmonic oscillator (quartic=%s)' % quartic)
pylab.savefig('plot_C1_matrixsquaring_beta%s.png' % beta)
pylab.show()
