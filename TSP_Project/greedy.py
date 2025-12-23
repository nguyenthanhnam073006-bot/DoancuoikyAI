# greedy.py
from utils import total_distance

def solve_tsp_greedy(cities, start=0):
    n = len(cities)
    visited = [False] * n
    path = [start]
    visited[start] = True

    current = start

    for _ in range(n - 1):
        nearest = None
        nearest_dist = float("inf")

        for i in range(n):
            if not visited[i]:
                dx = cities[current][0] - cities[i][0]
                dy = cities[current][1] - cities[i][1]
                dist = dx * dx + dy * dy  # không cần sqrt cho nhanh

                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = i

        visited[nearest] = True
        path.append(nearest)
        current = nearest

    # quay về thành phố xuất phát
    path.append(start)

    return path, total_distance(path, cities)