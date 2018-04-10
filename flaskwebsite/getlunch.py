from flask import Flask, render_template, request, send_file
import requests
import argparse
import json
import pprint
import sys
import random
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from flaskwebsite import getbusiness

# DUBLIN - Latitude: 53.3242381, Longitude:-6.385788
DEFAULT_LATITUDE = 53.3242381
DEFAULT_LONGITUDE = -6.385788
pp = pprint.PrettyPrinter(indent=3)
#TODO: no results template
#TODO: 404 page
#TODO: Create route w/ filter/ and query params
app = Flask(__name__)

@app.route("/") # decorator
def landing_page():
    return get_business_template("lunch")

@app.route("/<search_term>")
def get_business_template(search_term):
    # request.args is a dictionary with the url GET parameters
    latitude = request.args.get("latitude", DEFAULT_LATITUDE)
    longitude = request.args.get("longitude", DEFAULT_LONGITUDE)
    business_result = search_by_term(search_term, latitude, longitude)
    return render_template("index.html",
                            distance=round(business_result['distance'], 1),
                            search_term=search_term,
                            business_name=business_result['name'],
                            image_url=business_result['image_url'],
                            longitude=business_result['coordinates']['longitude'],
                            latitude=business_result['coordinates']['latitude'],)

def search_by_term(search_term, latitude, longitude):
    try:
        search_results = getbusiness.by_search_term(search_term, latitude, longitude)
        randindex = random.randint(0, (len(search_results) - 1))
        print(randindex)
        business = getbusiness.get_business_from_list(search_results, randindex)
        # pp.pprint(getbusiness.get_business_details(business['id']))
        #TODO: round distance number
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return business

# ajax
@app.route('/getbusiness/')
def get_business_ajax():
    latitude = request.args.get("latitude", DEFAULT_LATITUDE)
    longitude = request.args.get("longitude", DEFAULT_LONGITUDE)
    #print(f"TEST {request.args}")
    search_term = "lunch"
    business_result = search_by_term(search_term, latitude, longitude)
    return json.dumps(business_result)

@app.route("/about/") # decorator
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    # moved this here because of gunicorn error 98
    app.run(debug = True) #TODO: debug is iseful for development
                    #but shouldn't be used in production
