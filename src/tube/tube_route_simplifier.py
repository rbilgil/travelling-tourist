from collections import Counter

class TubeRouteSimplifier:

	@staticmethod
	def simplify(route, stations):
		route = TubeRouteSimplifier.chunk_route(route, stations)
		print route
		simple_route = [{ "from": "", "line": "" }]

		travel_directions = []
		for chunk in route:
			for index, stop in enumerate(chunk):
				travel_directions.append(stop[3])
				if index > 0:
					prev_line = chunk[index - 1][2]
					line = stop[2]
					if prev_line != line:
						direction, occurence = Counter(travel_directions).most_common(1)[0]
						travel_directions = []
						interchange_station = chunk[index - 1][0]
						simple_route[-1]["to"] = interchange_station
						simple_route[-1]["direction"] = direction + "-bound"
						simple_route.append({ "from": interchange_station, "line": stop[2] })
		return simple_route

	@staticmethod
	def explain(simple_route, stations):
		for index, node in enumerate(simple_route):
			if index == 0:
				print "Your routes for today:"
			if "to" in node:
				print node["line"].capitalize() + " line going " + node["direction"] + " from " + node["from"] + " to " + node["to"] + "."
			if not node["from"] in stations:
				print "Change to"

	@staticmethod
	def chunk_route(route, stations):
		chunks = []
		indices = []
		route_stops = [x[0] for x in route]
		for stop in stations:
			if stop in route_stops:
				indices.append(route_stops.index(stop))

		for first, second in zip(indices, indices[1:]):
			chunks.append(route[first:second])
		return chunks







