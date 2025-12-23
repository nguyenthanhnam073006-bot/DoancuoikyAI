import random
from utils import total_distance

def swap_sequence(p1, p2):
    seq = []
    temp = p1[:]
    for i in range(len(p1)):
        if temp[i] != p2[i]:
            j = temp.index(p2[i])
            seq.append((i, j))
            temp[i], temp[j] = temp[j], temp[i]
    return seq

def apply_swaps(path, swaps):
    p = path[:]
    for i, j in swaps:
        p[i], p[j] = p[j], p[i]
    return p

def solve_tsp_pso(cities, num_particles=30, iterations=200):
    n = len(cities)
    particles = []
    velocities = []
    pbest = []
    pbest_cost = []

    gbest = None
    gbest_cost = float("inf")

    for _ in range(num_particles):
        p = list(range(n))
        random.shuffle(p)
        p.append(p[0])
        particles.append(p)
        velocities.append([])
        pbest.append(p)
        cost = total_distance(p, cities)
        pbest_cost.append(cost)

        if cost < gbest_cost:
            gbest = p
            gbest_cost = cost

    for _ in range(iterations):
        for i in range(num_particles):
            r1, r2 = random.random(), random.random()
            v1 = swap_sequence(particles[i][:-1], pbest[i][:-1])
            v2 = swap_sequence(particles[i][:-1], gbest[:-1])

            new_velocity = v1[:int(r1 * len(v1))] + v2[:int(r2 * len(v2))]
            new_path = apply_swaps(particles[i][:-1], new_velocity)
            new_path.append(new_path[0])

            cost = total_distance(new_path, cities)
            particles[i] = new_path

            if cost < pbest_cost[i]:
                pbest[i] = new_path
                pbest_cost[i] = cost

                if cost < gbest_cost:
                    gbest = new_path
                    gbest_cost = cost

    return gbest, gbest_cost
# pso.py
import random
from utils import total_distance

class Particle:
    def __init__(self, num_cities):
        self.position = list(range(num_cities))
        random.shuffle(self.position)

        self.best_position = self.position[:]
        self.best_cost = float("inf")


def swap_sequence(a, b):
    """Tạo chuỗi swap để biến a → b"""
    a = a[:]
    swaps = []

    for i in range(len(a)):
        if a[i] != b[i]:
            j = a.index(b[i])
            swaps.append((i, j))
            a[i], a[j] = a[j], a[i]

    return swaps


def apply_swaps(position, swaps, prob=1.0):
    for i, j in swaps:
        if random.random() < prob:
            position[i], position[j] = position[j], position[i]


def solve_tsp_pso(
    cities,
    num_particles=30,
    max_iter=200,
    w=0.7,
    c1=1.5,
    c2=1.5
):
    num_cities = len(cities)

    swarm = [Particle(num_cities) for _ in range(num_particles)]
    global_best = None
    global_best_cost = float("inf")

    for _ in range(max_iter):
        for p in swarm:
            path = p.position + [p.position[0]]
            cost = total_distance(path, cities)

            # cập nhật best cá nhân
            if cost < p.best_cost:
                p.best_cost = cost
                p.best_position = p.position[:]

            # cập nhật global best
            if cost < global_best_cost:
                global_best_cost = cost
                global_best = p.position[:]

        # cập nhật particle
        for p in swarm:
            swaps_pbest = swap_sequence(p.position, p.best_position)
            swaps_gbest = swap_sequence(p.position, global_best)

            apply_swaps(p.position, swaps_pbest, prob=c1 / 2)
            apply_swaps(p.position, swaps_gbest, prob=c2 / 2)

    best_path = global_best + [global_best[0]]
    return best_path, global_best_cost
