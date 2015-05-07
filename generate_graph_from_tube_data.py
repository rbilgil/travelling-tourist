import json
import os.path
import re

from tube.graph import Graph
from tube.circle_distance import get_circle_distance


def text_to_tuple(line):
    return tuple(line.rstrip().strip("()").split(", "))


def convert_tube_data():
    tube = Graph()
    with open('tube_data/tube_edges.txt', "r") as f:
        for line in f:
            edge = text_to_tuple(line)

            if data_exists_for_stations(edge):
                start, end = get_more_data(edge)
                tube.add_vertex(edge[0], vertex_properties={"lat": start["lat"], "lon": start["lon"]})
                tube.add_vertex(edge[1], vertex_properties={"lat": end["lat"], "lon": end["lon"]})
                tube.add_edge(edge[0], edge[1], weight=get_edge_weight(start, end), edge_properties={"line": edge[2]})
    return tube


def data_exists_for_stations(edge):
    filename = get_filename_from_line(edge[2])
    return os.path.isfile(filename)


def get_filename_from_line(line):
    return "tube_data/individual_lines/" + line + ".json"


def get_more_data(edge):
    line = edge[2]
    points = []

    filename = get_filename_from_line(line)
    with open(filename, "r") as f:
        stations = json.loads(f.read())
        for station in stations:
            regex = r'\([^)]*\)'
            stationName = re.sub(regex, "", station["commonName"].strip().replace(" Underground Station", "").replace(
                " DLR Station", ""))
            if edge[0] == stationName:
                start = station
            elif edge[1] in stationName:
                end = station

    return start, end


def get_edge_weight(start, end):
    return get_circle_distance(get_lat_lon(start), get_lat_lon(end))


def get_lat_lon(station_name):
    return (station_name["lat"], station_name["lon"])


if __name__ == '__main__':
    tube = convert_tube_data()
    with open(get_filename_from_line("../tube_graph"), "w") as f:
        f.write(tube.as_json())