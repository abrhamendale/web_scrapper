#!/usr/bin/env python3
"""
Scrappes amazon
"""


from bs4 import BeautifulSoup
import requests
import time
from random import random
import requests, json, lxml
import sys

# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        if not title:
            title = soup.find("span", attrs={"id":'title'})
        # Inner NavigatableString Object
        title_value = title.string
        # Title as a string value
        title_string = title_value.strip()
        # # Printing types of values for efficient understanding
        # print(type(title))
        # print(type(title_value))
        # print(type(title_string))
        # print()
    except AttributeError:
        title_string = ""	
    return title_string
# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
        if price == 'Page 1 of 1':
            price = soup.find("span", attrs={'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).string.strip()
        if not price:
            price = 'Currently unavailable'
        #price = soup.find('span', {'id':"a-price-whole"}).text.strip()
    except AttributeError:
        try:
        # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except:		
            price = ""
    return price
# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()	
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	
    return rating
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""	
    return review_count
# Function to extract Availability Status
def get_availability(soup):
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
    print("amn")
    # Headers for request
    HEADERS = ({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"})
    ##{'User-Agent':
    #'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    #'Accept-Language': 'en-US'})*/

    # The webpage URL
    #URL = "https://www.amazon.com/s?k=&ref=nb_sb_noss_2"
    URL = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+item
    #URL = "https://www.amazon.com/s?k=" + item + "&crid=2PLVGX4VJVEWU&sprefix=gtx4090%2Caps%2C797&ref=nb_sb_noss_1"
    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    #print(webpage.content)
    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")
    print(webpage.content)
    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    # Store the links
    links_list = []
    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get('href'))
    print(len(links_list))
    # Loop for extracting product details from each link
    items_data = []
    for link in links_list:
        time.sleep(5 * random())
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")
        # Function calls to display all necessary product information
        price = get_price(new_soup)
        #if price:
        #    if ' to ' in price:
        #        price = float(price.split(' to ')[0][1:].replace(',', ''))
        #    else:
        #        price = float(price[1:].replace(',', ''))

        items_data.append({
                        'Website': 'Amazon',
                        'Link': 'https://www.amazon.com/' + link,
                        'Title': get_title(new_soup),
                        'Price[$]': price,
                        #'Condition': item_data['condition'],
                        'Top_rated': get_rating(new_soup),
                        'Reviews': get_review_count(new_soup),
                        'Availability': get_availability(new_soup),
                        #'buy_now_extention': exctention_buy_now,
                        #'Delivery': shipping,
                        #'location': location,
                        #'bids': {'count': bid_count, 'time_left': bid_time_left},
                        })
    return (json.dumps(items_data, indent = 2, ensure_ascii = False))
        #print("Product Title =", item_data.title)
        #print("Product Price =", item_data.Price)
        #print("Product Rating =", item_data.Rating)
        #print("Number of Product Reviews =", item_data.Product_reviews)
        #print("Availability =", item_data.Availability)
