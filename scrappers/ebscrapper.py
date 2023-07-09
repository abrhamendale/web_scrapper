#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests, json, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}


def eb_queuer(item):
    print("eb")
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw=' + item,
	headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    print(len(soup.select('.s-item__wrapper.clearfix')))
    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        if price:
            if ' to ' in price:
                price = float(price.split(' to ')[0][1:].replace(',', ''))
            else:
                price = float(price[1:].replace(',', ''))
        data.append({
            'Link': link,
            'Title': title,
            'Price[$]': price,
            'Condition': condition,
            'Top_rated': top_rated,
            'Reviews': reviews,
            'Availability': watchers_sold,
            #'buy_now_extention': exctention_buy_now,
            'Delivery': shipping,
            'Location': location,
            #'bids': {'count': bid_count, 'time_left': bid_time_left},
        })

    return (json.dumps(data, indent = 2, ensure_ascii = False))
#get_organic_results()
