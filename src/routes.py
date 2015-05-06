import os
from flask import Flask, render_template, jsonify, request
import foursquare_search
import urllib3.contrib.pyopenssl

app = Flask(__name__)
urllib3.contrib.pyopenssl.inject_into_urllib3()

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/places/search")
def search():
	query = request.args.get('query')
	fsq = foursquare_search.FoursquareSearch()
	results = fsq.search_venue(query)
	#return jsonify({"venues": results["venues"]})
	return jsonify({"query": query, "suggestions":
	[ 
		{ 
			"name": x["name"], 
			"address": x["location"]["formattedAddress"][0],
			"displayName": x["name"] + ", " + x["location"]["address"]
	    } for x in results["venues"]
    ] })

if __name__ == "__main__":
    app.run(debug=True)