import random
import math


class TravelingSalesman:
    def __init__(self, graph, vertices_to_visit, Tmax=1000.0, Tmin=1.0, steps=100):
        self.Tmax = Tmax  # Starting temp
        self.Tmin = Tmin  # Min temp
        self.steps = steps  # Max number of iterations
        self.graph = graph
        self.to_visit = vertices_to_visit
        self.best_path = (self.compute_distance(), self.to_visit)  # initially the best path is the user supplied path

    def get_path(self):
        self.anneal()
        return self.best_path

    def anneal(self):
        for T in self._get_temperature():
            self.move()
            old_dist = self.best_path[0]
            new_dist = self.compute_distance()
            if self._should_accept(new_dist, old_dist, T):
                # if accepting, the best path is now the swapped path
                self.best_path = (new_dist, self.to_visit)
            else:
                # if rejecting the swap, we restore the previous best path
                self.to_visit = self.best_path[1]

    def move(self):
        vertices = self.to_visit
        a = random.randint(0, len(vertices) - 1)
        b = random.randint(0, len(vertices) - 1)

        self.to_visit[a], self.to_visit[b] = self.to_visit[b], self.to_visit[a]

    def compute_distance(self):
        total_dist = 0
        for index, vertex in enumerate(self.to_visit):
            if index < len(self.to_visit) - 1:
                next = self.to_visit[index + 1]
                distance, path = self.graph.shortest_path(vertex, next)
                total_dist += distance

        return total_dist

    def _should_accept(self, weight, previous_weight, temperature):
        if weight < previous_weight:
            return 1.0
        else:
            p = math.exp(-abs(weight - previous_weight) / temperature)
            return random.random() < p

    def _get_temperature(self):
        T = self.Tmax
        step = 0
        while step < self.steps:
            alpha = math.exp(-math.log(self.Tmax / self.Tmin) / self.steps)
            yield T
            T = alpha * T
            step += 1