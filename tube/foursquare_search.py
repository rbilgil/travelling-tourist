import requests, json
requests.packages.urllib3.disable_warnings()


class FoursquareSearch:
    BASE_URL = "https://api.foursquare.com/v2/"
    urls = {
        "venue_search": "venues/search/"
    }

    def __init__(self, client_id, client_secret, version="20150506"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.version = version

    def get(self, url, payload):
        payload["client_id"] = self.client_id
        payload["client_secret"] = self.client_secret
        payload["v"] = self.version
        return requests.get(url, params=payload)

    def build_url(self, param):
        return self.BASE_URL + self.urls[param]

    def search_venue(self, venue_name):
        return json.loads(self.get(self.build_url("venue_search"), {'query': venue_name, 'near': 'London'}).text)["response"]
