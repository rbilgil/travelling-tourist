from graph import *
import unittest

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)

class TestGraph(unittest.TestCase):

	def setUp(self):
		self.g = Graph()
		self.g.reset()

	def test_add_vertex(self):
		self.g.add_vertex("A")
		self.assertTrue(self.g.has_vertex("A"))
		self.assertTrue(self.g.vertex_empty("A"))

	def test_add_edge(self):
		self.g.add_vertex("A")
		self.g.add_vertex("B")
		self.g.add_edge("A", "B")

		self.assertTrue(self.g.are_neighbours("A", "B"))
		self.assertTrue(self.g.are_neighbours("B", "A"))

	def test_add_directed_edge(self):
		self.g.add_vertex("K")
		self.g.add_vertex("Z")
		self.g.add_edge("K", "Z", directed = True)

		self.assertTrue(self.g.are_neighbours("K", "Z"))
		self.assertFalse(self.g.are_neighbours("Z", "K"))

	def test_are_connected(self):
		self.build_graph()

		self.assertTrue(self.g.are_connected("A", "C"))
		self.assertTrue(self.g.are_connected("A", "D"))
		self.assertFalse(self.g.are_connected("A", "E"))

	def build_graph(self):
		chars = list(char_range("A", "Z"))
		for char in chars:
			self.g.add_vertex(char)

		edges = [("A", "B"), ("A", "C"), ("B", "D"), ("D", "F"), ("D", "G")]
		for start, end in edges:
			self.g.add_edge(start, end)

	def test_vertices(self):
		self.build_graph()
		self.assertTrue(len(self.g.vertices()) > 0)

	def test_unconnected_graph(self):
		self.g.add_vertex("A")
		self.g.add_vertex("B")
		self.assertFalse(self.g.is_connected_graph())

	def test_connected_graph(self):
		self.build_graph()
		self.add_all_edges()
		self.assertFalse(self.g.is_connected_graph())

	def add_all_edges(self, weight = 0):
		chars = list(char_range("A", "Z"))
		for char in chars:
			self.g.add_edge("A", char, weight = weight)

	def test_get_edges(self):
		self.build_graph()
		weight = 5
		self.add_all_edges(weight)
		self.assertTrue(self.g.edges()[5][2] == weight)
	
if __name__ == '__main__':
    unittest.main()
	