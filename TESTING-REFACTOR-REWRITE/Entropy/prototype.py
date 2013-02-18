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
import numpy as np
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
    prob = [float(urlString.count(c)) / len(urlString) for c in dict.fromkeys(list(urlString))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy


def notBad(file_name):
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
        urlList.append({"urlentr": entropyRequestUrl, "fqdnentr": entropyFqdn, "pathentr": entropyPath, "searchentr": entropySearch})
    dataFrame = pandas.DataFrame.from_records(urlList)
    groupedBy = dataFrame.groupby('urlentr')
    uniqueValues = groupedBy.agg(lambda x: np.size(np.unique(x.values)))
    print
    print("NOT Malicious requestURL Strings Entropy Scores Analysis")
    print("====")
    print("Total Records Processed by Type: \n")
    print(dataFrame.count())
    print
    print("Unique Entropy Records Grouped by Key Value, RequestUrl Entropy: \n")
    print(uniqueValues)
    print
    print("Entropy Skew by Type: \n" + str(dataFrame.skew()))
    print
    print("Entropy Variance by Type: \n" + str(dataFrame.var()))
    print
    print("Entropy Kurtosis by Type: \n" + str(dataFrame.kurt()))
    print
    print("Entropy Standard Deviation by Type: \n" + str(dataFrame.std()))
    print
    print("Record Count by Type: \n" + str(dataFrame.count()))
    print
    print("The Mean Entropy by Type: \n" + str(dataFrame.mean()))
    print
    print("The Max Entropy by Type: \n" + str(dataFrame.max()))
    print
    print("The Min Entropy by Type: \n" + str(dataFrame.min()))
    print
    print("The Mean Absolute Deviation by Type: \n" + str(dataFrame.mad()))
    print
    lowerBound = (dataFrame.groupby('urlentr')['urlentr'].count().head(n=10)[:1])
    upperBound = (dataFrame.groupby('urlentr')['urlentr'].count().tail(n=10)[9:10])
    print
    print("Malicious Request URL Entropy Score Analysis")
    print("====")
    print("requestUrl Lower & Upper Bounds:")
    print("=====")
    print("Lower Bound: \n" + str(lowerBound))
    print
    print("Upper Bound: \n" + str(upperBound))
    print
    topTen = (dataFrame.groupby('urlentr')['urlentr'].count().tail(n=10))
    bottomTen = (dataFrame.groupby('urlentr')['urlentr'].count().head(n=10))
    print("Top Ten Entropy requestUrl Scores:")
    print(topTen)
    print
    print("Bottom Ten Entropy requestUrl Scores:")
    print(bottomTen)


def Malicious():
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
    groupedBy = dataFrame.groupby('urlentr')
    uniqueValues = groupedBy.agg(lambda x: np.size(np.unique(x.values)))
    print
    print("Total Records Processed by Type: \n")
    print(dataFrame.count())
    print
    print("Unique Entropy Records Grouped by Key Value, RequestUrl Entropy: \n")
    print(uniqueValues)
    print
    print("Entropy Skew by Type: \n" + str(dataFrame.skew()))
    print
    print("Entropy Variance by Type: \n" + str(dataFrame.var()))
    print
    print("Entropy Kurtosis by Type: \n" + str(dataFrame.kurt()))
    print
    print("Entropy Standard Deviation by Type: \n" + str(dataFrame.std()))
    print
    print("Record Count by Type: \n" + str(dataFrame.count()))
    print
    print("The Mean Entropy by Type: \n" + str(dataFrame.mean()))
    print
    print("The Max Entropy by Type: \n" + str(dataFrame.max()))
    print
    print("The Min Entropy by Type: \n" + str(dataFrame.min()))
    print
    print("The Mean Absolute Deviation by Type: \n" + str(dataFrame.mad()))
    print
    lowerBound = (dataFrame.groupby('urlentr')['urlentr'].count().head(n=10)[:1])
    upperBound = (dataFrame.groupby('urlentr')['urlentr'].count().tail(n=10)[9:10])
    print("requestUrl Lower & Upper Bounds:")
    print("=====")
    print("Lower Bound: \n" + str(lowerBound))
    print
    print("Upper Bound: \n" + str(upperBound))
    print
    topTen = (dataFrame.groupby('urlentr')['urlentr'].count().tail(n=10))
    bottomTen = (dataFrame.groupby('urlentr')['urlentr'].count().head(n=10))
    print("Top Ten Entropy requestUrl Scores:")
    print(topTen)
    print
    print("Bottom Ten Entropy requestUrl Scores:")
    print(bottomTen)


def main():
    #file_name = "history.txt"
    #notBad(file_name)
    Malicious()

if __name__ == '__main__':
    main()