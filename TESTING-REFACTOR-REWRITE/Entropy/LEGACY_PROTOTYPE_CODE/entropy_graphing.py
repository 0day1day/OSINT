__date__ = "2/6/2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"

"""TODO: Utilizes malc0de RSS Feed Instead of scraping main website: http://malc0de.com/rss/
Utilize Python XML parsing module: import xml.etree.ElementTree as ET
"""

import requests, math, types, pandas
import numpy as np
from urlparse import urlparse
from bs4 import BeautifulSoup

def notMalicious(file_name):
    for requestUrl in open(file_name, 'r'):
        yield requestUrl

def maliciousLinks(html):
    soup = BeautifulSoup(html)
    i = 0
    for table in soup.findAll('table', {"class": "prettytable"}):
        for rows in table.findAll('tr'):
            for index,cell in enumerate(rows.findAll('td')):
                if index == 1:
                    text = ''
                    for e in cell.recursiveChildGenerator():
                        if isinstance(e, types.StringTypes):
                            text += e.strip()
                    yield text

def malCodeUrl():
    """Cull MD5 Hash Values from www.malc0de.com"""
    for i in range(1, 100):
        request_Url = "http://malc0de.com/database/?&page=" + str(i)
        r = requests.get(request_Url)
        for item in maliciousLinks(r.text):
            yield item

def calcEntropy(urlString):
    """Calculate Entropy for a requestURL String
       First Obtain the probability of the characters within the requestURL String
       Then Calculate The Entropy of the String
    """
    prob = [ float(urlString.count(c)) / len(urlString) for c in dict.fromkeys(list(urlString)) ]
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy


def graphMalicious():
    urlList = []
    for requestUrl in malCodeUrl():
        parsedUrl = urlparse("http://" + requestUrl.encode('ascii', 'ignore'))
        fullUrl = "http://" + requestUrl.encode('ascii', 'ignore')
        urlFqdn = parsedUrl[1]
        urlPath = parsedUrl[2]
        urlSearch = parsedUrl[4]
        entropyRequestUrl = abs(calcEntropy(fullUrl.encode('ascii', 'ignore')))
        entropyFqdn = abs(calcEntropy(urlFqdn))
        entropyPath = abs(calcEntropy(urlPath))
        entropySearch = abs(calcEntropy(urlSearch))
        urlList.append({ "urlentr": entropyRequestUrl, "fqdnentr": entropyFqdn, "pathentr": entropyPath, "searchentr": entropySearch })
    dataFrame = pandas.DataFrame.from_records(urlList)
    #dataFrame['fqdnentr'].plot(color='b', figsize=(20,9), title=("Entropy Malicious RequestUrl FQDN Strings"))
    #dataFrame['pathentr'].plot(color='r', figsize = (20,9), title = ("Entropy Malicious RequestUrl Path Strings"))
    #dataFrame['searchentr'].plot(color='g', figsize = (20,9), title = ("Entropy Malicious RequestUrl Search Strings"))
    #dataFrame['urlentr'].plot(color='b', figsize = (20,9), title = ("Entropy Malicious RequestUrl URL Strings"))
    dataFrame.plot(subplots=True, figsize = (20,9), title = ("Entropy Malicious All Elements"))

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
    dataFrame.plot(subplots=True, figsize = (20,9), title = ("Entropy NOT-Malicious All Elements"))

def main():
    file_name = "history.txt"
    #graphMalicious()
    graphNotMalicious(file_name)

if __name__ == '__main__':
    main()