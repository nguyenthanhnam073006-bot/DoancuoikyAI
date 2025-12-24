import heapq
import math
from functools import lru_cache
from utils import build_distance_matrix

class AStarTSP:
    def __init__(self, dist_matrix):
        self.dist = dist_matrix
        self.n = len(dist_matrix)
        self.start = 0

    def heuristic(self, current, visited):
        unvisited = [i for i in range(self.n) if i not in visited]
        
        if not unvisited:
            return self.dist[current][self.start]

        h = 0
        h += self.mst_cost(tuple(unvisited))
        h += min(self.dist[current][u] for u in unvisited)
        h += min(self.dist[u][self.start] for u in unvisited)
        
        return h

    @lru_cache(maxsize=None)
    def mst_cost(self, nodes_tuple):
        nodes = list(nodes_tuple)
        if len(nodes) <= 1:
            return 0

        visited = {nodes[0]}
        cost = 0

        while len(visited) < len(nodes):
            min_edge = math.inf
            next_node = None

            for u in visited:
                for v in nodes:
                    if v not in visited and self.dist[u][v] < min_edge:
                        min_edge = self.dist[u][v]
                        next_node = v

            visited.add(next_node)
            cost += min_edge

        return cost

    def solve(self):
        pq = []
        start_state = (0, frozenset([self.start]), self.start, [self.start])
        heapq.heappush(pq, start_state)

        best_cost = {}

        while pq:
            f, visited, current, path = heapq.heappop(pq)
            g = sum(self.dist[path[i]][path[i+1]] for i in range(len(path)-1))

            if (current, visited) in best_cost and best_cost[(current, visited)] <= g:
                continue
            best_cost[(current, visited)] = g

            if len(visited) == self.n:
                total_cost = g + self.dist[current][self.start]
                return path + [self.start], total_cost

            for nxt in range(self.n):
                if nxt not in visited:
                    new_visited = visited | {nxt}
                    h = self.heuristic(nxt, new_visited)
                    new_g = g + self.dist[current][nxt]
                    heapq.heappush(
                        pq,
                        (new_g + h, new_visited, nxt, path + [nxt])
                    )

        return None, math.inf

def solve_tsp_astar(cities):
    dist_matrix = build_distance_matrix(cities)
    tsp = AStarTSP(dist_matrix)
    return tsp.solve()