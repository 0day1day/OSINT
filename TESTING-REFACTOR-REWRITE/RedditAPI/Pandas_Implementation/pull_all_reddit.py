import requests
from bs4 import BeautifulSoup

def extract_hrefs(html):
    """Generic function to extract href links within HTML"""
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    for element in links:
        yield element

def process_html(request_Url):
    """Process URL to cull hrefs"""
    r = requests.get(request_Url)
    for item in extract_hrefs(r.text):
        if "/r" in item:
            yield(item)

"""Return list of items from a sub-reddit of reddit.com."""

from urllib2 import urlopen, HTTPError
from json import JSONDecoder

def getitems( subreddit, previd=''):
    """Return list of items from a subreddit."""
    url = 'http://www.reddit.com/r/%s.json' % subreddit
    # Get items after item with 'id' of previd.
    if previd != '':
        url = '%s?after=t3_%s' % (url, previd)
    try:
        json = urlopen( url ).read()
        data = JSONDecoder().decode( json )
        items = [ x['data'] for x in data['data']['children'] ]
    except HTTPError as ERROR:
        print '\tHTTP ERROR: Code %s for %s.' % (ERROR.code, url)
        items = []
    return items

if __name__ == "__main__":

    print 'Recent items for Python.'
    ITEMS = getitems( 'NSA' )
    for ITEM in ITEMS:
        print '\t%s - %s' % (ITEM['title'], ITEM['url'])
