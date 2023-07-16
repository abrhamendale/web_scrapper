#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests, json, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def get_condition(item):
    """
    Extracts the review count.
    """
    try:
        condition = item.select_one('.SECONDARY_INFO').text
    except:
        condition = None
    return condition


def get_shipping(item):
    """
    Extracts the shipping.
    """
    try:
        shipping = item.select_one('.s-item__logisticsCost').text
    except:
        shipping = None
    return shipping


def get_location(item):
    """
    Extracts the location.
    """
    try:
        location = item.select_one('.s-item__itemLocation').text
    except:
        location = None
    return location


def get_watchers(item):
    """
    Extracts the shipping.
    """
    try:
        watchers_sold = item.select_one('.NEGATIVE').text
    except:
        watchers_sold = None
    return watchers_sold


def get_rating(item):
    """
    Extracts the shipping.
    """
    if item.select_one('.s-item__etrs-badge-seller') is not None:
        top_rated = True
    else:
        top_rated = False
    return top_rated


def get_reviews(item):
    """
    Extracts the reviews.
    """
    try:
        reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
    except:
        reviews = None
    return reviews


def get_price(item):
    """
    Extracts the price.
    """
    try:
        price = item.select_one('.s-item__price').text
    except:
        price = None
    if price:
        if ' to ' in price:
            price = float(price.split(' to ')[0][1:].replace(',', ''))
        else:
            price = float(price[1:].replace(',', ''))
    return price


def eb_queuer(item):
    """
    Extracts data from search results.
    """
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw=' + item,
	headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    data = []
    print('Ebay:', len(soup.select('.s-item__wrapper.clearfix')))
    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        data.append({
            'Website': 'Ebay',
            'Link': link,
            'Title': title,
            'Price[$]': get_price(item),
            'Condition': get_condition(item),
            'Top_rated': get_rating(item),
            'Reviews': get_reviews(item),
            'Availability': get_watchers(item),
            'Delivery': get_shipping(item),
            'Location': get_location(item),
        })
    return (json.dumps(data, indent = 2, ensure_ascii = False))
