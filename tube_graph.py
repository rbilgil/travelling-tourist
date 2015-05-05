import json
import math
from graph import Graph

def read_tube_data():
	with open("tube_data/individual_lines/victoria.json", "r") as f:
		data = sorted(json.loads(f.read()), key = lambda stop: stop["lat"])
	
	stations = [x["commonName"] for x in data]
	return stations, data

def get_distance(start, end):
	
	# assume earth is roughly flat between tube stations
	distance = math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

	return distance


def get_circle_distance(start, end):
	x = get_lat_lon(start)
	y = get_lat_lon(end)
	degrees_to_radians = math.pi / 180.0
	d_2_r = degrees_to_radians # for brevity
	radius_of_earth = 6371 # in km
	
	# phi = 90 - latitude
	phi = ((90.0 - x[0])*d_2_r, (90 - y[0])*d_2_r)
         
	# theta = longitude
	theta = (x[1] * d_2_r, y[1] * d_2_r)
         
	# Spherical distance from spherical coordinates.
	cos = (math.sin(phi[0])*math.sin(phi[1])*math.cos(theta[0] - theta[1]) + math.cos(phi[0])*math.cos(phi[1]))
	arc = math.acos(cos)

	return arc * radius_of_earth

def get_lat_lon(station_name):
	return ((station["lat"], station["lon"]) for station in data if station["commonName"] == station_name).next()
	
stations, data = read_tube_data()

graph = Graph()
for index, station in enumerate(stations):
	graph.add_vertex(station)
	if index > 0:
		graph.add_edge(station, stations[index - 1], weight = get_circle_distance(station, stations[index - 1]))

print graph.edges()