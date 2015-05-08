class TubeRouteSimplifier:
    def __init__(self, routes, stations_to_visit):
        self.to_visit = stations_to_visit
        self.routes = routes

    def get_simplified_routes(self):
        simplified_routes = []

        for index, route in enumerate(self.routes):
            simplified_route = self.simplify_route(self.to_visit[index], route)
            simplified_routes.append(simplified_route)

        return simplified_routes

    @staticmethod
    def simplify_route(starting_station, route):
        simplified_route = [{"from": starting_station}]

        stops_counter = 0
        distance_counter = 0
        for index, (prev, next) in enumerate(zip(route, route[1:])):
            prev_line, next_line = prev[2], next[2]
            distance_counter += prev[1]
            stops_counter += 1
            if next_line != prev_line:
                simplified_route[-1]["to"] = prev[0]
                simplified_route[-1]["line"] = prev[2]
                simplified_route[-1]["direction"] = prev[3]
                simplified_route[-1]["distance"] = round(distance_counter, 2)
                simplified_route[-1]["time"] = round(distance_counter/30.0*60.0, 2)
                simplified_route[-1]["stops"] = stops_counter
                simplified_route.append({"from": prev[0]})
                distance_counter = 0
                stops_counter = 0

        if len(route):
            last = {"to": route[-1][0], "line": route[-1][2], "direction": route[-1][3], "stops": stops_counter, "distance": round(distance_counter, 2), "time": round(distance_counter/30.0*60.0, 2)}
            for key, val in last.iteritems():
                simplified_route[-1][key] = val

        return simplified_route










