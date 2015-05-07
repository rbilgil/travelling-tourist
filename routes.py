from flask import Flask, render_template, jsonify, request
from tube.tube_path_finder import TubePathFinder

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
    path, simple_routes = path_finder.get_path()
    sorted_locations = path_finder.sort_locations(locations, path)

    return jsonify({"locations": sorted_locations, "route": simple_routes})


if __name__ == "__main__":
    app.run(debug=True)