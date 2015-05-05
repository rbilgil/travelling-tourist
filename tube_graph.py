import json
import math
import re
from glob import glob
from graph import Graph

files = glob("tube_data/individual_lines/*.json")

def read_tube_data(files):
	data = {}
	for file in files:
		with open(file, "r") as f:
			print file
			line_name = re.search(r"([a-zA-Z]+)\.json", file).group(1)
			data[line_name] = sorted(json.loads(f.read()), key = lambda stop: stop["lat"])
	
	return data

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
	return (station_name["lat"], station_name["lon"])

if __name__ == '__main__':

	data = read_tube_data(files)
	graph = Graph()
	for line, stations in data.iteritems():
		for index, station in enumerate(stations):
			graph.add_vertex(station["commonName"])
			if index > 0:
				graph.add_edge(station["commonName"], stations[index - 1]["commonName"], weight = get_circle_distance(station, stations[index - 1]), edge_properties = { "line": line })

	print graph.edges()