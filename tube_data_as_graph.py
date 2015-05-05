from graph import Graph
from random import randint
from traveling_salesman import TravelingSalesman
filename = "tube_data/tube_graph.json"

def tube_data_as_graph():	
	tube = Graph()
	tube.from_json_file(filename)

	return tube

if __name__ == '__main__':
	tube = tube_data_as_graph()
	vertices = tube.vertices()
	#random stops
	stops = []
	for i in range(15):
		vertex = None
		while not vertex in stops:
			vertex = vertices[randint(0, len(vertices) - 1)]
			stops.append(vertex)
		
	print stops
	salesman = TravelingSalesman(tube, stops)
	print salesman.get_path()
