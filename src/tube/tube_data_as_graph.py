from graph import Graph
from random import randint
from traveling_salesman import TravelingSalesman

def tube_file_to_graph(filename):
	tube = Graph()
	tube.from_json_file(filename)

	return tube

