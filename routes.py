from flask import Flask, render_template, jsonify, request
from tube.tube_path_finder import TubePathFinder
import math
from tube.foursquare_search import FoursquareSearch


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/places/search")
def place_search():
    query = request.args.get('query')
    fsq = FoursquareSearch(client_id='H1BQ3S15DUHOWQHWVCLYU3CRPB4PT3PEY1UOCT5VQJN3RDOC',
                           client_secret='OTYNTC5XYJT2BUDBEIFUB50DRK313LYKQA05EDSFKYX5OWE4')
    results = fsq.search_venue(query)

    return jsonify({"query": query, "suggestions": [x for x in results["venues"]]})


@app.route("/route", methods=["POST"])
def get_route():
    data = request.get_json().get('places')
    locations = dict((x, (y, z)) for x, y, z in data)
    coords = [(x[1], x[2]) for x in data]
    path_finder = TubePathFinder(coords)
    path, simple_routes, distance, stations = path_finder.get_path()
    sorted_locations = path_finder.sort_locations(locations, path)
    walking_distances = [path_finder.closest_station_to(lat, lon)[1] for name, (lat, lon) in sorted_locations]
    walking_speed = 5
    walking_time = round(reduce(lambda acc, dist: acc + dist, walking_distances) / walking_speed * 60.0, 1)
    return jsonify({
        "locations": sorted_locations,
        "route": simple_routes,
        "totalDistance": round(distance),
        "totalTime": round(distance/30.0*60.0, 2) + walking_time,
        "walkingDistances": walking_distances
    })


if __name__ == "__main__":
    app.run(debug=True)