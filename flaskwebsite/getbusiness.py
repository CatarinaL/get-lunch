# CFG Python at DIT - group project
# Kompal and Catarina
# this file deals with access to Yelp and google geolocation APIs
# partially BASED on yelp-fusion/fusion/python/sample.py
# -*- coding: utf-8 -*-

import argparse
import json
import pprint
import requests
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

pp = pprint.PrettyPrinter(indent=3)

# API constants, we shouldn't have to change these...
# unless we need different paths, but we can just add more here, like transactions
#TODO: generate new API key for use in production website
API_KEY= 'zd2uwmgCgOAh4tq7X4XlO6Otfk64uUIPRjk3S6-aLK2U98pJdD27bPslfqNtV_Z5FYrGmsO9xvq65DMUHpOvDk8700Fwon4_vZImf7riM2kofgYdeut1zZtiXhO6WnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash
# Defaults
DEFAULT_TERM = 'lunch'
SEARCH_LIMIT = 7

# user/request location
def get_location():
    #TODO: try catch exceptions and errors
    location_response = requests.post(LOCATION_API)
    # pp.pprint(location_response.json())
    return location_response.json()

# compose request to Fusion API - returns json response
def api_request(host, path, url_params=None):
    if url_params is None:
        url_params = {}
    # "or {}": if url_params isn't created, use an empty dictionary
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    # header with value Bearer API_KEY is required
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    #pp.pprint(response)
    return response.json()

#search path - returns top (SEARCH_LIMIT) results
def search(search_term, latitude, longitude):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the api_request.
    """

    url_params = {
        'sort_by': "distance", #TODO: fix?, sort is not working
        'term': search_term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude, #replace is just a string function, in this case to take care of our whitespace and substitute them by + so the url works
        'limit': SEARCH_LIMIT,
        'open_now': True, # we only want open places
        'price': "1,2,3",
        'radius': 1500,
    }
    #request returns full json response for results of query
    #pp.pprint(api_request(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params))
    return api_request(API_HOST, SEARCH_PATH, url_params=url_params)

def query_api(search_term, latitude, longitude):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(search_term, latitude, longitude)
    pp.pprint(response)
    businesses = response.get('businesses')

    #TODO: change default location to name of city using lat long parameters
    if not businesses:
        print(f"No businesses for {search_term} found in your location." +\
        "Don\'t be such a fussy eater!")
        return

    print('{0} businesses found'.format(len(businesses)))

    return businesses


def by_search_term(search_term, latitude, longitude):
    try:
        response = query_api(search_term, latitude, longitude)
        return response
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

def get_business_from_list(businesses, index=0):
    """Selects from business list by index

    Args:
        businesses (list): list of businesses returned by query_api()
        index (int): The index of object in list
    """
    return businesses[index]

def get_distance(businesses, index=0):
    """Returns distance of selected business

    Args:
        businesses (list): list of businesses returned by query_api()
        index (int): The index of object in list
    """
    distance = businesses[index]['distance']
    return distance


#returns more detailed info on one business
def get_business_details(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the api_request.
    """
    business_path = BUSINESS_PATH + business_id

    return api_request(API_HOST, business_path, API_KEY)
