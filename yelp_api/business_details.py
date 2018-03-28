# CFG Python at DIT - group project
# Kompal and Catarina
# partially BASED on yelp-fusion/fusion/python/sample.py
# -*- coding: utf-8 -*-

import argparse
import json
import pprint
import requests
import sys
import urllib
# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode
pp = pprint.PrettyPrinter(indent=4)

#TODO: generate new API key for use in production website
API_KEY= 'zd2uwmgCgOAh4tq7X4XlO6Otfk64uUIPRjk3S6-aLK2U98pJdD27bPslfqNtV_Z5FYrGmsO9xvq65DMUHpOvDk8700Fwon4_vZImf7riM2kofgYdeut1zZtiXhO6WnYx'
LOCATION_PATH= 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyA8xV5zsXFHbbG_cDrN2XrxNOW8f1f34xc'
# API constants, we shouldn't have to change these...
# unless we need different paths, but we can just add more here, like transactions
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults
DEFAULT_TERM = 'lunch'
DEFAULT_LOCATION = 'Dublin, IE'
SEARCH_LIMIT = 3

#location
def get_location():
    #TODO: try catch exceptions and errors
    location_response = requests.post(LOCATION_PATH)
    print(location_response.url)
    pp.pprint(location_response.json())
    print(location_response.status_code)
    print(location_response.headers["content-type"])
    return location_response.json()

# request to Fusion API - returns json response
def request(host, path, api_key, url_params=None):
    if url_params is None:
        url_params = {}
    # "or {}": if url_params isn't created, use an empty dictionary
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    # headers with value Bearer API_KEY is required
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    print(u'Business URL: {0}'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    pprint.pprint(response, indent=3)
    return response.json()

def search(api_key, term, latitude, longitude):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'sort-by': "distance", #TODO: fix, sort not working
        'term': term.replace(' ', '+'),
        'latitude': latitude.replace(' ', '+'),
        'longitude': longitude.replace(' ', '+'), #replace is just a string function, in this case to take care of our whitespace and substitute them by + so the url works
        'limit': SEARCH_LIMIT,
        'open-now': "true", # we only want open places
        'price': "1,2,3",
        'radius': '1500',
    }
    #request returns full json response for top 3 results
    pprint.pprint(request(API_HOST, SEARCH_PATH, api_key, url_params=url_params), indent=3)
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)



def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, latitude, longitude):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, latitude, longitude)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found. Don\'t be such a fussy eater!'.format(term, location))
        return

    #TODO: TEST -is it sorting by distance? apparently not
    for i in range(0, 3):
        business_distance= businesses[i]['distance']
        print(str(business_distance) + "m")

    #return only first result
    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def main():
    #parser = argparse.ArgumentParser()

    #parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        #type=str, help='Search term (default: %(default)s)')
    #parser.add_argument('-l', '--location', dest='location',
                        #default=DEFAULT_LOCATION, type=str,
                        #help='Search location (default: %(default)s)')

    #input_values = parser.parse_args()

    location = get_location()
    latitude = str(location['location']['lat'])
    longitude = str(location['location']['lng'])

    try:
        return query_api(DEFAULT_TERM, latitude, longitude)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
