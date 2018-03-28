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

@app.route("/") # decorator
def landing_page():
    return render_template("index.html", title = "Where to lunch?")

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

# Create route w/ filter/ and query params

app.run(debug = True) #TODO: debug is iseful for development
                    #but shouldn't be used in production
