import math
import json

from tube.robin_queue import Queue
from tube.robin_queue import PriorityQueue


class Graph:
    graph = {}
    weights = {}
    edge_properties = {}
    vertex_properties = {}

    def as_json(self):
        return json.dumps([
            self.graph,
            self.weights,
            self.edge_properties,
            self.vertex_properties
        ])

    def from_json(self, data):
        obj = json.loads(data)
        self.graph = obj[0]
        self.weights = obj[1]
        self.edge_properties = obj[2]
        self.vertex_properties = obj[3]

    def from_json_file(self, file):
        with open(file, "r") as f:
            self.from_json(f.read())

    def reset(self):
        self.graph = {}
        self.weights = {}
        self.edge_properties = {}
        self.vertex_properties = {}

    def vertices(self):
        return self.graph.keys()

    def edges(self):
        edges = []
        for vertex in self.vertices():
            for neighbour in self.get_neighbours(vertex):
                edges.append({"from": vertex, "to": neighbour, "weight": self.get_weight(vertex, neighbour),
                              "properties": self.get_edge_properties(vertex, neighbour)})
        return edges

    def get_weight(self, start, end):
        weight_index = self.graph[start].index(end)
        return self.weights[start][weight_index]

    def get_edge_properties(self, start, end):
        edge_index = self.graph[start].index(end)
        return self.edge_properties[start][edge_index]

    def get_vertex_properties(self, vertex):
        return self.vertex_properties[vertex]

    def add_vertex(self, vertex, vertex_properties={}):
        if not self.has_vertex(vertex):
            self.graph[vertex] = []
            self.weights[vertex] = []
            self.edge_properties[vertex] = []
            self.vertex_properties[vertex] = vertex_properties

    def has_vertex(self, vertex):
        return vertex in self.vertices()

    def vertex_empty(self, vertex):
        if self.has_vertex(vertex):
            return len(self.graph[vertex]) == 0
        else:
            return True

    def add_edge(self, start, end, directed=False, weight=0,
                 edge_properties={}):  # pass in any additional edge info as a hash
        if self.has_vertex(start) and self.has_vertex(end):
            if not start == end and not self.has_edge(start, end):
                self.graph[start].append(end)
                self.weights[start].append(weight)
                self.edge_properties[start].append(edge_properties)
                if not directed:
                    self.graph[end].append(start)
                    self.weights[end].append(weight)
                    self.edge_properties[end].append(edge_properties)
        else:
            raise Exception("Vertex " + start + " or " + end + " doesn't exist")

    def has_edge(self, start, end):
        return end in self.get_neighbours(start)

    def are_neighbours(self, start, end):
        return self.has_edge(start, end)

    def get_neighbours(self, vertex):
        return self.graph[vertex]

    def are_connected(self, start, end):
        return end in self.bfs(start)

    def is_connected_graph(self):
        vertices = self.vertices()
        for vertex in vertices:
            traversal = self.bfs(vertex)
            if len(traversal) == len(vertices) - 1:
                return False
        return True

    def bfs(self, current_node):
        visited = []
        queue = Queue()
        queue.enqueue(current_node)
        visited.append(current_node)

        while not queue.empty():
            current_node = queue.dequeue()
            for neighbour in self.get_neighbours(current_node):
                if not neighbour in visited:
                    queue.enqueue(neighbour)
                    visited.append(neighbour)

        return visited

    def generate_route(self, path):
        routes = []

        # for pairs of stops, we generate a separate route
        for prev, next in zip(path, path[1:]):
            routes.append(self.shortest_path(prev, next)[1])

        return routes

    def shortest_path(self, start, end):  # uses dijkstra
        distances = {start: 0}
        previous_vertices = {}
        queue = PriorityQueue()

        for v in self.vertices():
            if v != start:
                distances[v] = float("inf")
            queue.queue(v, distances[v])

        while not queue.empty():
            weight, u = queue.dequeue()
            for v in self.get_neighbours(u):
                alternate_distance = distances[u] + self.get_weight(u, v)

                if v in previous_vertices:
                    if self.has_change_cost(u, v, previous_vertices[v]):
                        alternate_distance *= 1.5  #increase cost by 50% for line change

                if alternate_distance < distances[v]:
                    distances[v] = alternate_distance
                    previous_vertices[v] = u
                    queue.queue(v, alternate_distance)

        trace = end
        path = []
        while trace in previous_vertices:
            next = previous_vertices[trace]
            path.insert(0, self._get_path_tuple(trace, next))
            trace = next

        total_dist = sum([x[1] for x in path])
        return total_dist, path

    def _get_path_tuple(self, start, end):
        return (start, self.get_weight(start, end), self.get_edge_properties(start, end)["line"],
                self.get_direction(start, end))

    def has_change_cost(self, prev, current, next):
        # if we have to change lines, add a kilometer to weight
        if self.get_edge_properties(prev, current)["line"] != self.get_edge_properties(current, next)["line"]:
            return True
        else:
            return False

    def get_direction(self, start, end):
        start_coord = (self.get_vertex_properties(start)["lat"], self.get_vertex_properties(start)["lon"])
        end_coord = (self.get_vertex_properties(end)["lat"], self.get_vertex_properties(end)["lon"])

        bearing = int(self.compass_bearing(start_coord, end_coord))
        directions = ["East", "South", "West", "North"]

        direction = directions[(bearing / 45) % 4]

        return direction

    @staticmethod
    def compass_bearing(start, end):
        if (type(start) != tuple) or (type(end) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(start[0])
        lat2 = math.radians(end[0])

        longitude_diff = math.radians(end[1] - start[1])

        x = math.sin(longitude_diff) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                               * math.cos(lat2) * math.cos(longitude_diff))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180 to + 180 which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing