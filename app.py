#!/usr/bin/env python3
"""
Scrapper runner
"""


from scrappers.amnscrapper import amn_queuer
from scrappers.nescrapper import ne_queuer
from scrappers.ebscrapper import eb_queuer
from operator import itemgetter
from flask import Flask, render_template, request, url_for, flash, redirect
import json
import pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd06f1655ea4849c29263b14ce972d533d588cf11c4855a3d'


def scrap(key):
    """
    Scraps the available websites.
    """
    ne_queuer(key)
    #print(eb_queuer('Galaxy%20S23%20Black'))
    scrappers = json.loads(eb_queuer(key)) + json.loads(amn_queuer(key))
    scrappers = scrappers + json.loads(ne_queuer(key))
    items = [x for x in scrappers if isinstance(x, dict)]
    for i in items:
        #print('-----------', i['Availability'])
        if i['Availability'] == 'Not available':
            remove(i)
        try:
            float(i['Price[$]'])
        except:
            i['Price[$]'] = 0
    items.sort(key=itemgetter('Price[$]'))
    return items


@app.route('/', methods=['GET'])
def index():
    return render_template('web_index.html')


@app.route('/', methods=['POST'])
def input():
    title = request.form['title']
    print(title)
    if not title:
        flash('Title is required!')
    return redirect('/' + title)


@app.route('/<string:key>', methods=['GET'])
def search(key):
    print(key)
    if key:
        items = scrap(key)
    return render_template('web_index.html', posts=items)
