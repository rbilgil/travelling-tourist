from random import randint
import os

from tube.tube_data_as_graph import tube_file_to_graph
from tube.traveling_salesman import *
from tube.tube_station_finder import TubeStationFinder
from tube.tube_route_simplifier import TubeRouteSimplifier


class TubePathFinder:
    # route_coords is array of lat/lon tuples e.g. [(51.5, -0.16), (51.4, -0.14)] etc.
    def __init__(self, route_coords):
        self.tube_graph = tube_file_to_graph(
            os.path.dirname(os.path.realpath(__file__)) + "/../tube_data/tube_graph.json")
        self.route_coords = route_coords

    def get_path(self):
        stations = list(set(
            [self.closest_station_to(*val)[0] for val in self.route_coords]))  # the list(set()) removes duplicate stations
        distance, path = self._traveling_salesman(stations)
        routes = self.tube_graph.generate_route(path)
        route_simplifier = TubeRouteSimplifier(routes, stations)
        simple_routes = route_simplifier.get_simplified_routes()

        return path, simple_routes, distance, stations

    def closest_station_to(self, lat, lon):
        finder = TubeStationFinder(self.tube_graph)
        return finder.closest_to(lat, lon)

    def _random_stops(self):
        vertices = self.tube_graph.vertices()
        stops = []
        for i in range(15):
            vertex = None
            while not vertex in stops:
                vertex = vertices[randint(0, len(vertices) - 1)]
                stops.append(vertex)
        return stops

    def _traveling_salesman(self, stops):
        salesman = TravelingSalesman(self.tube_graph, stops)
        distance, path = salesman.get_path()
        return distance, path

    def sort_locations(self, locations, path):
        sorted_locations = range(len(path))
        for key, location in locations.iteritems():
            sorted_locations[path.index(self.closest_station_to(*location)[0])] = (key, location)

        return sorted_locations