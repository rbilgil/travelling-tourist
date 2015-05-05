import requests, json

tube_lines = [u'bakerloo', u'central', u'circle', u'district', u'hammersmith-city', u'jubilee', u'metropolitan', u'northern', u'piccadilly', u'victoria', u'waterloo-city']

for line in tube_lines:
	stops = json.loads(requests.get("http://api.tfl.gov.uk/Line/%7Bids%7D/StopPoints?ids=" + line + "&app_id=&app_key=").text)
	relevant_data = [
		{ "lat": x["lat"] , "lon": x["lon"], "id": x["id"], "commonName": x["commonName"], "placeType": x["placeType"], "icsCode": x["icsCode"] } for x in stops
	]
	with open(line + '.json', 'w') as outfile:
	    json.dump(relevant_data, outfile)




