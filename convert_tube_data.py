from graph import Graph
import json, math, os.path, re

def text_to_tuple(line):
	return tuple(line.rstrip().strip("()").split(", "))

def convert_tube_data():
	tube = Graph()
	with open('tube_data/tube_edges.txt', "r") as f:
		for line in f:
			edge = text_to_tuple(line)
			
			if data_exists_for_stations(edge):
				tube.add_vertex(edge[0])
				tube.add_vertex(edge[1])
				tube.add_edge(edge[0], edge[1], weight = get_edge_weight(edge), edge_properties = { "line": edge[2]})
	return tube

def data_exists_for_stations(edge):
	filename = get_filename_from_line(edge[2])
	return os.path.isfile(filename)
			
def get_filename_from_line(line):
	return "tube_data/individual_lines/" + line + ".json"

def get_edge_weight(edge):
	line = edge[2]
	points = []

	filename = get_filename_from_line(line)
	with open(filename, "r") as f:
		stations = json.loads(f.read())
		for station in stations:
			regex = r'\([^)]*\)'
			stationName = re.sub(regex, "", station["commonName"].strip().replace(" Underground Station", ""))
			if edge[0] == stationName:
				start = station
			elif edge[1] in stationName:
				end = station
	
	return get_circle_distance(start, end)


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
	tube = convert_tube_data()
	with open(get_filename_from_line("../tube_graph"), "w") as f:
		f.write(tube.as_json())