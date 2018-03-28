from flask import Flask, render_template, request, send_file
import requests
import getbusiness
import argparse
import json
import pprint
import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

app = Flask(__name__)

#TODO: no results template
#TODO: 404 page
#TODO: Create route w/ filter/ and query params

@app.route("/") # decorator
def landing_page():
    try:
        response = getbusiness.search_term("lunch")['name']
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return render_template("index.html", search_term = "lunch", business_name = response)


@app.route("/<search_term>/")
def search_by_term(search_term):
    try:
        response = getbusiness.search_term(search_term)['name']
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    return render_template("index.html", search_term = search_term, business_name = response)

app.run(debug = True) #TODO: debug is iseful for development
                    #but shouldn't be used in production
