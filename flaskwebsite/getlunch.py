from flask import Flask, render_template, request, send_file
import requests
import argparse
import json
import pprint
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from flaskwebsite import getbusiness

# Latitude: 53.3242381, Longitude:-6.385788
DEFAULT_LATITUDE = "53.3242381"
DEFAULT_LONGITUDE = "-6.385788"
#TODO: no results template
#TODO: 404 page
#TODO: Create route w/ filter/ and query params
app = Flask(__name__)

@app.route("/") # decorator
def landing_page():
    return search_by_term("lunch")

@app.route("/<search_term>/")
def search_by_term(search_term):
    try:
        latitude = request.args.get("latitude", DEFAULT_LATITUDE)
        longitude = request.args.get("longitude", DEFAULT_LONGITUDE)
        search_results = getbusiness.by_search_term(search_term, latitude, longitude)
        business = getbusiness.get_business_from_list(search_results, 1)
        business_name = business['name']
        image_url = business['image_url']
        #TODO: round distance number
        distance = business['distance']
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return render_template("index.html", distance=distance, search_term = search_term, business_name = business_name, image_url=image_url)


if __name__ == "__main__":
    # moved this here because of gunicorn error 98
    app.run(debug = True) #TODO: debug is iseful for development
                    #but shouldn't be used in production
