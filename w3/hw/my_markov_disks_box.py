import random
import math
import pylab
import os


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


def load_cache(filename, sigma, N):
    if os.path.isfile(filename):
        f = open(filename, 'r')
        L = []
        for line in f:
            a, b = line.split()
            L.append([float(a), float(b)])
        f.close()
        print('starting from file', filename)
    else:
        L = []
        N_sqrt = int(N**0.5)
        delxy = max(1/N, sigma)
        two_delxy = 2*delxy
        for k in range(N):
            L = [[delxy + i * two_delxy, delxy + j * two_delxy] for i in range(N_sqrt) for j in range(N_sqrt)]
        print('starting from a new random configuration')
    return L


def save_cache(filename):
    with open(filename, 'w') as f:
        for a in L:
            f.write(str(a[0]) + ' ' + str(a[1]) + '\n')


if __name__ == '__main__':
    N = 64
    eta = 0.72
    n_steps = 10000
    # eta = N * (pi * sigma ** 2)
    sigma = math.sqrt(eta/(N*math.pi))
    delta = 0.5*sigma
    filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
    L = load_cache(filename, sigma, N)
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
    save_cache(filename)
    show_conf(L, sigma, 'hello', '1.png')
