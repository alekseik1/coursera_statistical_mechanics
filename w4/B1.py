import random
import pylab
import math


def markov(dim, n_trials, delta=0.1):
    coords = [0.]*dim
    prev_radius = 0.
    n_hits = 0
    for i in range(n_trials):
        k = random.randint(0, dim-1)
        coords_new = coords.copy()
        coords_new[k] = coords_new[k] + random.uniform(-delta, delta)
        new_radius = prev_radius + coords_new[k]**2 - coords[k]**2
        if new_radius < 1.:
            prev_radius = new_radius
            coords[:] = coords_new
    return coords


dim = 20
hist_data = [markov(dim, 10**3) for _ in range(1000)]
hist_data = [math.sqrt(sum(point[k]**2 for k in range(dim))) for point in hist_data]
x_array = [i/1000. for i in range(1000)]
y_array = [20*x**19 for x in x_array]
pylab.plot(x_array, y_array)
pylab.hist(hist_data, bins=100, density=True)
pylab.xlabel('r')
pylab.ylabel('Density')
pylab.savefig('1.png')
pylab.show()
pylab.close()
