__date__ = "2/6/2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"

import feedparser, requests

def getMalUrls(rss_feed):
    getRssFeed = feedparser.parse(rss_feed)
    for items in getRssFeed.entries:
        item = items.summary_detail.value.encode('ascii', 'ignore').split(',')[0].split(' ')[1]
        yield item

def getVxUrls(url_vxstring):
    request_urlGet = requests.get(url_vxstring)
    if request_urlGet.status_code == 200:
        data = request_urlGet.text
        yield data

def getMalWareDomains(url_mdstring):
    request_urlGet = requests.get(url_mdstring)
    if request_urlGet.status_code == 200:
        data = request_urlGet.text
        yield data


def main():
    url_mdstring = 'http://mirror1.malwaredomains.com/files/BOOT'
    element = "PRIMARY"
    for item in getMalWareDomains(url_mdstring):
        if item.startswith(element):
            print(item)
    # url_vxstring = 'http://vxvault.siri-urz.net/URL_List.php'
    # for item in getVxUrls(url_vxstring):
    #     print(item)
    #     if item.startswith("h"):
    #         print(item)
    # rss_feed = 'http://malc0de.com/rss/'
    # for element in getMalUrls(rss_feed):
    #     print("http://" + element)

if __name__ == '__main__':
    main()
