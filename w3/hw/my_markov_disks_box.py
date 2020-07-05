import random
import math
import pylab
import cmath
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


def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)


if __name__ == '__main__':
    N = 64
    eta_array = [x / 100. for x in range(72, 19, -2)]
    psi_array = []
    for eta in eta_array:
        print('eta', eta)
        n_steps = 10000
        # eta = N * (pi * sigma ** 2)
        sigma = math.sqrt(eta / (N * math.pi))
        delta = 0.5 * sigma
        filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
        L = load_cache(filename, sigma, N)
        history = []
        for steps in range(n_steps):
            if steps % 100 == 0:
                history.append(abs(Psi_6(L, sigma)))
            current_particle = random.choice(L)
            current_particle_next = [current_particle[0] + random.uniform(-delta, delta),
                                     current_particle[1] + random.uniform(-delta, delta)]
            min_dist = min(dist(other_particle, current_particle_next)
                           for other_particle in L if other_particle != current_particle)
            # No overlap, move is accepted
            if min_dist >= 2*sigma:
                current_particle[:] = current_particle_next
                L = [[p[0] % 1.0, p[1] % 1.0] for p in L]
        psi_array.append(sum(history)/len(history))
    pylab.plot(eta_array, psi_array)
    pylab.savefig('eta.png')
    pylab.xlabel('eta')
    pylab.ylabel('|psi_6|')
    pylab.title('|psi_6| (eta)')
    pylab.show()
    pylab.close()
