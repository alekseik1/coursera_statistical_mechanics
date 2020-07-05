import random
import math
import pylab


def show_conf(L, sigma, title, fname):
    """
    >>> show_conf(L, sigma, 'test graph', 'one_disk.png')
    """
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='b')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()


def dist(x, y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return math.sqrt(d_x**2 + d_y**2)


if __name__ == '__main__':
    N = 4
    L = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
    # eta = N * (pi * sigma ** 2)
    eta = 0.5
    sigma = math.sqrt(eta/(N*math.pi))
    delta = 0.1
    n_steps = int(1e4)
    for steps in range(n_steps):
        current_particle = random.choice(L)
        current_particle_next = [current_particle[0] + random.uniform(-delta, delta),
                                 current_particle[1] + random.uniform(-delta, delta)]
        min_dist = min(dist(other_particle, current_particle_next)
                       for other_particle in L if other_particle != current_particle)
        # No overlap, move is accepted
        if min_dist >= 2*sigma:
            current_particle[:] = current_particle_next
            L = [[p[0] % 1.0, p[1] % 1.0] for p in L]
    show_conf(L, sigma, 'hello', '1.png')
