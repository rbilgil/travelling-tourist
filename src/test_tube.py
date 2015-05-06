from tube.tube_data_as_graph import tube_file_to_graph
from tube.traveling_salesman import *
from tube.tube_station_finder import TubeStationFinder
from tube.tube_route_simplifier import TubeRouteSimplifier
from random import randint
import os


def get_random_stops(tube_graph):
	vertices = tube_graph.vertices()
	stops = []
	for i in range(15):
		vertex = None
		while not vertex in stops:
			vertex = vertices[randint(0, len(vertices) - 1)]
			stops.append(vertex)
	return stops

def test_traveling_salesman(tube_graph, stops):
	salesman = TravelingSalesman(tube_graph, stops)
	path = salesman.get_path()
	print path
	return path

def test_closest_station(tube_graph, lat, lon):
	finder = TubeStationFinder(tube_graph)
	return finder.closest_to(lat, lon)

if __name__ == '__main__':
	tube_graph = tube_file_to_graph(os.path.dirname(os.path.realpath(__file__)) + "/../tube_data/tube_graph.json")
	coords = {
		"Knightsbridge": (51.500503, -0.160972),
		"Covent Garden": (51.510867, -0.124398),
		"Old Spitalfields": (51.519840, -0.081826),
		"Canary Wharf": (51.504180, -0.016637),
		"Hyde Park": (51.506771, -0.159850),
		"Wembley Stadium": (51.556321, -0.283789),
		"London Eye": (51.502633, -0.119533),
		"Westminster Abbey": (51.497396, -0.124940),
		"Heathrow Airport": (51.469495, -0.424661)
	}

	stations = []
	for key, val in coords.iteritems():
		stations.append(test_closest_station(tube_graph, *val)[0])

	stations = get_random_stops(tube_graph)
	print

	path = test_traveling_salesman(tube_graph, stations)[1]
	route = tube_graph.generate_route(path)
	simple_route = TubeRouteSimplifier.simplify(route, stations)
	
	for route in simple_route:
		print (route["from"], route["to"], route["line"], route["direction"])
	#print TubeRouteSimplifier.explain(simple_route, stations)




		
