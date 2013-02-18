# -*- coding: utf-8 -*-

'''
Twitter woeid listing
https://api.twitter.com/1/trends/available.json?lat=37.781157&long=-122.400612831116

Global Keys for Yahoo! Where On Earch ID
====
placeType
woeid
name
countryCode
parentid
url
country
====

'''

__author__ = 'AlienOne'

import json, twitter, requests, re
from operator import itemgetter

def json_global_keys(search_url):
    SEARCH_BASE = search_url
    request_url = SEARCH_BASE
    request_urlGet = requests.get(request_url)
    if request_urlGet.status_code == 200:
        if 'json' in (request_urlGet.headers['content-type']):
            data = json.loads(request_urlGet.text)
            data_list = data
            a_list = []
            for item in sorted((set(item) for item in data_list), key=len, reverse=True):
                if not any(item.issubset(Q) for Q in a_list):
                    a_list.append(item)
                    for element in a_list:
                        for product in element:
                            yield(product)

def woeid_codes(search_url):
    SEARCH_BASE = search_url
    SEARCH_BASE2 = "https://api.twitter.com/1/trends/15015370.json"
    woeid_string = re.findall(r'\d+\.', SEARCH_BASE2)[0]
    woeid_strip = woeid_string.split('.')
    woeid_int = int(woeid_strip[0])
    request_url = SEARCH_BASE
    request_urlGet = requests.get(request_url)
    if request_urlGet.status_code == 200:
        if 'json' in (request_urlGet.headers['content-type']):
            data = json.loads(request_urlGet.text)
            data_list = data
            for element in data_list:
                if element['countryCode'] != None:
                    ##print(element['woeid'])
                    if woeid_int == element['woeid']:
                        yield(element['countryCode'].lower() + ',' + str(element['woeid']))

# Global Variables
search_url = 'http://api.twitter.com/1/trends/available.json?lat=37.781157&long=-122.400612831116'

# Define Main
def main():
    for element in woeid_codes(search_url):
        # Yield Country Code + woeid
        print(element.split(',')[0] + ',' + element.split(',')[1])

# Main Execution
if __name__ == '__main__':
    main()