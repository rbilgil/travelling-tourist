from robin_queue import Queue
from robin_queue import PriorityQueue
from heapq import *
import json

class Graph:
	graph = {}
	weights = {}
	edge_properties = {}

	def as_json(self):
		return json.dumps([
			self.graph,
			self.weights,
			self.edge_properties
		])

	def from_json(self, data):
		obj = json.loads(data)
		self.graph = obj[0]
		self.weights = obj[1]
		self.edge_properties = obj[2]

	def from_json_file(self, file):
		with open(file, "r") as f:
			self.from_json(f.read())

	def reset(self):
		self.graph = {}
		self.weights = {}
		self.edge_properties = {}

	def vertices(self):
		return self.graph.keys()

	def edges(self):
		edges = []
		for vertex in self.vertices():
			for neighbour in self.get_neighbours(vertex):
				edges.append({ "from": vertex, "to": neighbour, "weight": self.get_weight(vertex, neighbour), "properties": self.get_edge_properties(vertex, neighbour)})
		return edges

	def get_weight(self, start, end):
		weight_index = self.graph[start].index(end)
		return self.weights[start][weight_index]

	def get_edge_properties(self, start, end):
		edge_index = self.graph[start].index(end)
		return self.edge_properties[start][edge_index]

	def add_vertex(self, vertex):
		if not self.has_vertex(vertex):
			self.graph[vertex] = []
			self.weights[vertex] = []
			self.edge_properties[vertex] = []

	def has_vertex(self, vertex):
		return vertex in self.vertices()

	def vertex_empty(self, vertex):
		if self.has_vertex(vertex):
			return len(self.graph[vertex]) == 0
		else:
			return True

	def add_edge(self, start, end, directed = False, weight = 0, edge_properties = {}): # pass in any additional edge info as a hash
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


	def shortest_path(self, start, end): #uses dijkstra
		distances = { start: 0 }
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
				if alternate_distance < distances[v]:
					distances[v] = alternate_distance
					previous_vertices[v] = u
					queue.queue(v, alternate_distance)

		trace = previous_vertices[end]
		path = []
		while trace in previous_vertices:
			next = previous_vertices[trace]
			path.insert(0, (trace, self.get_weight(trace, next), self.get_edge_properties(trace, next)["line"]))
			trace = next

		total_dist = sum([x[1] for x in path])
		return total_dist, path





