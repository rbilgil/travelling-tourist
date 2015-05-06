import foursquare

class FoursquareSearch:

	def __init__(self):
		self.client = foursquare.Foursquare(client_id='H1BQ3S15DUHOWQHWVCLYU3CRPB4PT3PEY1UOCT5VQJN3RDOC', client_secret='OTYNTC5XYJT2BUDBEIFUB50DRK313LYKQA05EDSFKYX5OWE4')

	def search_venue(self, venue_name):
		return self.client.venues.search(params={'query': venue_name, 'near': 'London'})


	