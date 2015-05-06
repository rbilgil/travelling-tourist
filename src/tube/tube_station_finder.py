from tube.circle_distance import get_circle_distance

class TubeStationFinder:
	def __init__(self, tube_graph):
		self.graph = tube_graph

	def closest_to(self, lat, lon):
		stops = self.graph.vertices()
		closest = { "stop": None, "distance": float("inf") } #initialise closest as far away
		for stop in stops:
			coords = self.graph.get_vertex_properties(stop)
			distance = get_circle_distance((coords["lat"], coords["lon"]), (lat, lon))
			if distance <= closest["distance"]:
				closest["distance"] = distance
				closest["stop"] = stop

		return closest["stop"], closest["distance"]

