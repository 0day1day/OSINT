# -*- coding: utf-8 -*-
'''
Twitter Trends Developer Notes
====

NOTE => you can mashup any web application JSON query with Twitter Trends that supports Yahoo! WOEID

http://developer.yahoo.com/geo/geoplanet/
https://dev.twitter.com/docs/api/1/get/trends/%3Awoeid

Global Keys
===
locations => [{'woeid': 1, 'name': 'Worldwide'}]quer

created_at => 2012-07-14T05:19:00Z

trends => break down in tuples to group by keys 

('url', 'query', 'name', 'promoted_content', 'events')

as_of
===
Twitter API woeid
https://dev.twitter.com/docs/api/1/get/trends/%3Awoeid

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

Twitter JSON WOEID Trend Call
https://api.twitter.com/1/trends/2427032.json

Notice at the end of the JSON query => [{"name":"Indianapolis","woeid":2427032}]}]

Utilized the Google API - $20/month for x number of transactions 

HowTo Get API Keys
====
http://www.am3yrus.com/index.php/tutorials/10-siriserver-installation/18-how-to-get-the-api-keys

'''
__author__ = 'AlienOne'

import json, twitter, requests, re

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

def json_local_keys(search_url):
    SEARCH_BASE = search_url
    request_url = SEARCH_BASE
    request_urlGet = requests.get(request_url)
    if request_urlGet.status_code == 200:
        if 'json' in (request_urlGet.headers['content-type']):
            data = json.loads(request_urlGet.text)
            data_list = data[0]["trends"]
            a_list = []
            for item in sorted((set(item) for item in data_list), key=len, reverse=True):
                if not any(item.issubset(Q) for Q in a_list):
                    a_list.append(item)
                    for element in a_list:
                        for product in element:
                            yield(product)
            
def twitter_trending(search_url, woeid):
    SEARCH_BASE = search_url + str(woeid) + ".json"
    request_url = SEARCH_BASE
    request_urlGet = requests.get(request_url)
    if request_urlGet.status_code == 200:
        if 'json' in (request_urlGet.headers['content-type']):
            data = json.loads(request_urlGet.text)
            data_list = data[0]["trends"]
            for element in data_list:
                regex = r'^\d\d|\W\d\d'
                replace = r' '
                yield((element['name'])+ ',' + re.sub(regex, replace, (element['query'])) + ',' + (element['url']))

class Main():
    def print_global_keys():
        for keys in json_global_keys(search_url):
            print(keys)
    
    def print_local_keys():
        for keys in json_local_keys(search_url):
            print(keys)
    def print_global_keys2():
        search_url = search_url3
        for keys in json_global_keys(search_url):
            print(keys)
    def print_trending():
        search_url = search_url2
        for item in twitter_trending(search_url, woeid):
            print(item)
    
# Global Variables
search_url = 'http://api.twitter.com/1/trends/1.json'
search_url2 = 'http://api.twitter.com/1/trends/'
search_url3 = 'http://api.twitter.com/1/trends/available.json?lat=37.781157&long=-122.400612831116'

# Main Execution
print("====")
print("Dumping JSON Data Structure Global Keys for Twitter Global Trends")
print("====")
Main.print_global_keys()
print("====")
print("Finished Dumping JSON Global Keys")
print("====")
print("Dumping JSON Data Structure Local Keys for Twitter Global Trends")
print("====")
Main.print_local_keys()
print("====")
print("Finished Dumping JSON Local Keys")
print("====")
print("Dumping Current Twitter US Trending Topics")
print("====")
woeid = 15015370
Main.print_trending()
print("====")
print("Finished Printing Twitter Global Trending Topics")
print("====")
print("Global Keys for Yahoo! Where On Earch ID")
print("====")
Main.print_global_keys2()

    
    