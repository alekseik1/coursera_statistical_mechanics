import numpy as np
import pylab


def rho_free(x, xp, beta):
    return np.exp(-(x - xp) ** 2 / (2.0 * beta))/np.sqrt(2.0 * np.pi * beta)


def rho_harmonic_trotter(grid, beta):
    xx, pp = np.meshgrid(grid, grid)
    return rho_free(xx, pp, beta)*np.exp(-0.5 * beta * 0.5 * (xx ** 2 + pp ** 2))


x_max = 8
dx = 10**-1
x = np.arange(-x_max, x_max+dx, dx)
beta_tmp = 2.0 ** (-6)
beta = 2.0 ** 2
rho = rho_harmonic_trotter(x, beta_tmp)
while beta_tmp < beta:
    rho = np.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0
    print('beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp))

Z = np.trace(rho)*dx
pi_of_x = np.diag(rho)/Z
f = open('data_harm_matrixsquaring_beta' + str(beta) + '.dat', 'w')
for j in range(len(x)):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()


def pi_quant(x, beta):
    return np.exp(-x ** 2 * np.tanh(beta / 2.0)) * np.sqrt(np.tanh(beta / 2.0) / np.pi)


pylab.plot(x, pi_of_x, label='matrix-squaring')
pylab.plot(x, pi_quant(x, beta), label='analytical')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\pi(x)$')
pylab.title('Matrix-squaring, beta=%s' % beta)
pylab.savefig('plot_B1_matrixsquaring_beta%s.png' % beta)
pylab.show()
