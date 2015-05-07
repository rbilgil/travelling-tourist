import json

from tube.foursquare_search import FoursquareSearch


if __name__ == '__main__':
    locations = {
        "Knightsbridge": (51.500503, -0.160972),
        "Covent Garden": (51.510867, -0.124398),
        "Old Spitalfields": (51.519840, -0.081826),
        "Canary Wharf": (51.504180, -0.016637),
        "Hyde Park": (51.506771, -0.159850),
        "Wembley Stadium": (51.556321, -0.283789),
        "London Eye": (51.502633, -0.119533),
        "Westminster Abbey": (51.497396, -0.124940),
        "Heathrow Airport": (51.469495, -0.424661)
    }

    # path_finder = TubePathFinder(locations.values())
    # path, simple_routes = path_finder.get_path()
    # sorted_locations = path_finder.sort_locations(locations, path)

    # print sorted_locations, path
    fsq = FoursquareSearch(client_id='H1BQ3S15DUHOWQHWVCLYU3CRPB4PT3PEY1UOCT5VQJN3RDOC',
                           client_secret='OTYNTC5XYJT2BUDBEIFUB50DRK313LYKQA05EDSFKYX5OWE4')
    print fsq.search_venue("coffee")["venues"][0]