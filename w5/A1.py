import random
import math
import pylab


def psi_0_sq(x):
    return 1/math.sqrt(math.pi) * math.exp(-x**2)


x = 0.0
delta = 0.5
hist_data = []
for k in range(100000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < psi_0_sq(x_new)/psi_0_sq(x):
        x = x_new
    hist_data.append(x)

pylab.hist(hist_data, bins=100, density=True, label='histgram')
x_data = [i/1000. for i in range(-3000, 3001)]
y_data = [psi_0_sq(x) for x in x_data]
pylab.plot(x_data, y_data, label='analytical')
pylab.xlabel('x')
pylab.ylabel(r'$\psi^2$')
pylab.title(r'$\psi^2$ histogram and curve')
pylab.legend()
pylab.savefig('A1.png')
pylab.show()
pylab.close()
