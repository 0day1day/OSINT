__date__ = "2/6/2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"

import math, pandas, feedparser
from urlparse import urlparse

def notMalicious(file_name):
    for requestUrl in open(file_name, 'r'):
        yield requestUrl

def maliciousLinks(rss_feed):
    getRssFeed = feedparser.parse(rss_feed)
    for items in getRssFeed.entries:
        item = items.summary_detail.value.encode('ascii', 'ignore').split(',')[0].split(' ')[1]
        yield item

def calcEntropy(urlString):
    """Calculate Entropy for a requestURL String
       First Obtain the probability of the characters within the requestURL String
       Then Calculate The Entropy of the String
    """
    prob = [ float(urlString.count(c)) / len(urlString) for c in dict.fromkeys(list(urlString)) ]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy


def graphMalicious():
    urlList = []
    rss_feed = 'http://malc0de.com/rss/'
    for requestUrl in maliciousLinks(rss_feed):
        parsedUrl = urlparse("http://" + requestUrl.encode('ascii', 'ignore'))
        fullUrl = "http://" + requestUrl.encode('ascii', 'ignore')
        urlFqdn = parsedUrl[1]
        urlPath = parsedUrl[2]
        urlSearch = parsedUrl[4]
        entropyRequestUrl = abs(calcEntropy(fullUrl.encode('ascii', 'ignore')))
        entropyFqdn = abs(calcEntropy(urlFqdn))
        entropyPath = abs(calcEntropy(urlPath))
        entropySearch = abs(calcEntropy(urlSearch))
        urlList.append({"urlentr": entropyRequestUrl, "fqdnentr": entropyFqdn, "pathentr": entropyPath, "searchentr": entropySearch})
    dataFrame = pandas.DataFrame.from_records(urlList)
    #dataFrame['fqdnentr'].plot(color='b', figsize=(20,9), title=("Entropy Malicious RequestUrl FQDN Strings"))
    #dataFrame['pathentr'].plot(color='r', figsize = (20,9), title = ("Entropy Malicious RequestUrl Path Strings"))
    #dataFrame['searchentr'].plot(color='g', figsize = (20,9), title = ("Entropy Malicious RequestUrl Search Strings"))
    #dataFrame['urlentr'].plot(color='b', figsize = (20,9), title = ("Entropy Malicious RequestUrl URL Strings"))
    #dataFrame.plot(subplots=True, figsize = (20,9), title = ("Entropy Malicious All Elements - Grid View"))
    dataFrame.plot(figsize = (20,9), title = ("Entropy Malicious All Elements"))

def graphNotMalicious(file_name):
    urlList = []
    for requestUrl in notMalicious(file_name):
        parsedUrl = urlparse(requestUrl.encode('ascii', 'ignore'))
        urlFqdn = parsedUrl[1]
        urlPath = parsedUrl[2]
        urlSearch = parsedUrl[4]
        entropyRequestUrl = abs(calcEntropy(parsedUrl))
        entropyFqdn = abs(calcEntropy(urlFqdn))
        entropyPath = abs(calcEntropy(urlPath))
        entropySearch = abs(calcEntropy(urlSearch))
        urlList.append({ "urlentr": entropyRequestUrl, "fqdnentr": entropyFqdn, "pathentr": entropyPath, "searchentr": entropySearch })
    dataFrame = pandas.DataFrame.from_records(urlList)
    #dataFrame['fqdnentr'].plot(color='b', figsize=(20,9), title=("Entropy NOT-Malicious RequestUrl FQDN Strings"))
    #dataFrame['pathentr'].plot(color='r', figsize = (20,9), title = ("Entropy NOT-Malicious RequestUrl Path Strings"))
    #dataFrame['searchentr'].plot(color='g', figsize = (20,9), title = ("Entropy NOT-Malicious RequestUrl Search Strings"))
    #dataFrame['urlentr'].plot(color='b', figsize = (20,9), title = ("Entropy NOT-Malicious RequestUrl URL Strings"))
    #dataFrame.plot(subplots=True, figsize = (20,9), title = ("Entropy NOT-Malicious All Elements - Grid View"))
    dataFrame.plot(figsize = (20,9), title = ("Entropy NOT-Malicious All Elements"))

def main():
    file_name = "history.txt"
    graphMalicious()
    #graphNotMalicious(file_name)

if __name__ == '__main__':
    main()