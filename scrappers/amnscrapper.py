#!/usr/bin/env python3
"""
Scrappes for amazon.
"""


from bs4 import BeautifulSoup
import requests
import time
from random import random
import requests, json, lxml
import sys


def get_title(soup):
    """
    Extracts the title.
    """
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        if not title:
            title = soup.find("span", attrs={"id":'title'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""	
    return title_string


def get_price(soup):
    """
    Extracts the price.
    """
    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
        if price == 'Page 1 of 1':
            price = soup.find("span", attrs={'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).string.strip()
        if not price:
            price = 'Currently unavailable'
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except:		
            price = ""
    return price


def get_rating(soup):
    """
    Extracts the rating.
    """
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()	
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	
    return rating


def get_review_count(soup):
    """
    Extracts the review count.
    """
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""	
    return review_count


def get_availability(soup):
    """
    Extracts the availability information.
    """
    try:
        available = soup.find("div", attrs={'ID':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"	
    return available	


def amn_queuer(item):
    """
    Runs a function for every item data required.
    """
    HEADERS = ({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                "Accept-Encoding":"gzip, deflate",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests":"1"})
    URL = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+item
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
    print('Amazon:',len(links_list))
    items_data = []
    for link in links_list:
        time.sleep(5 * random())
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        price = get_price(new_soup)
        if price:
            if ' to ' in price:
                price = float(price.split(' to ')[0][1:].replace(',', ''))
            else:
                price = float(price[1:].replace(',', ''))
        items_data.append({
                        'Website': 'Amazon',
                        'Link': 'https://www.amazon.com/' + link,
                        'Title': get_title(new_soup),
                        'Price[$]': price,
                        'Top_rated': get_rating(new_soup),
                        'Reviews': get_review_count(new_soup),
                        'Availability': get_availability(new_soup),
                        })
    return (json.dumps(items_data, indent = 2, ensure_ascii = False))
