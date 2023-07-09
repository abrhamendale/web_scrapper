#!/usr/bin/env python3
"""
Scrapper runner
"""


from scrappers.amnscrapper import amn_queuer
from scrappers.ebscrapper import eb_queuer
from operator import itemgetter
from flask import Flask, render_template
import json
import pprint


app = Flask(__name__)


def scrap(key):
    """
    Scraps the available websites.
    """
    #print(eb_queuer('Galaxy%20S23%20Black'))
    items = [x for x in json.loads(eb_queuer(key)) if isinstance(x, dict)]
    for i in items:
        #print('-----------', i['Availability'])
        if i['Availability'] == 'Not available':
            remove(i)
    items.sort(key=itemgetter('Price[$]'))
    return items


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<key>', methods=['GET', 'POST'])
def search(key):
    items = scrap(key)
    return render_template('index.html', posts=items)
