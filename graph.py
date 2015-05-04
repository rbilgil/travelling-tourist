from queue import Queue

class Graph:
	graph = {}
	weights = {}

	def reset(self):
		self.graph = {}

	def vertices(self):
		return self.graph.keys()

	def edges(self):
		edges = []
		for vertex in self.vertices():
			for neighbour in self.get_neighbours(vertex):
				edges.append((vertex, neighbour, self.get_weight(vertex, neighbour)))
		return edges

	def get_weight(self, start, end):
		weight_index = self.graph[start].index(end)
		return self.weights[start][weight_index]

	def add_vertex(self, vertex):
		if not self.has_vertex(vertex):
			self.graph[vertex] = []
			self.weights[vertex] = []

	def has_vertex(self, vertex):
		return vertex in self.vertices()

	def vertex_empty(self, vertex):
		if self.has_vertex(vertex):
			return len(self.graph[vertex]) == 0
		else:
			return True

	def add_edge(self, start, end, directed = False, weight = 0):
		if self.has_vertex(start) and self.has_vertex(end):
			if not start == end and not self.has_edge(start, end):
				self.graph[start].append(end)
				self.weights[start].append(weight)
				if not directed:
					self.graph[end].append(start)
					self.weights[end].append(weight)
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

			if len(traversal) < vertices:
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
