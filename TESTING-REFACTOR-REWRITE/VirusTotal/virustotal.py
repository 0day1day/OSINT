__date__ = "Nov 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import csv
import datetime
import requests
import time
import os
import feedparser
from bs4 import BeautifulSoup


def getMalCode(rss_feed):
    """Get www.malc0de.com RSS Feed Elements"""
    getRssFeed = feedparser.parse(rss_feed)
    for items in getRssFeed.entries:
        item = items.summary_detail.value.encode('ascii', 'ignore').split(',')
        yield item


def getMalValues(rss_feed):
    """Dump Malcode Values Into a Dictionary DataStructure"""
    for element in getMalCode(rss_feed):
        if 'rtf' in element[1]:
            continue
        requesturl = element[0].split(' ')[1]
        ipaddress = element[1].split(':')[1]
        countrycode = element[2].split(' ')[2]
        asn = element[3].split(' ')[2]
        md5 = element[4].split(' ')[2]
        keys = ["RequestURL", "IPAddress", "CountryCode", "ASN", "MD5"]
        values = [requesturl, ipaddress, countrycode, asn, md5]
        malDict = dict(zip(keys, values))
        yield malDict


def virusTotalTest(csv_filename, rss_feed):
    """Utilize VirusTotal Public API"""
    f = csv.writer(open(csv_filename, "ab+"))
    for items in getMalValues(rss_feed):
        request_Url = "https://www.virustotal.com/vtapi/v2/file/report"
        parameters = {"resource": items['MD5'],
                      "apikey": "5dff9055f2785dafbf43ef4ec02828130ec2b0ac10b218158b7c371f4e1ed5c9"}
        r1 = requests.get(request_Url, params=parameters)
        data = r1.json()
        if data is not None:
            if data["response_code"] == 1:
                if data["positives"] <= 15:
                    r = requests.get(data["permalink"])
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text)
                        rows = soup.findAll("div", {"class": "row"})
                        for row in rows:
                            element = row.findAll("td", {})
                            element_rend = ["".join(x.renderContents().strip(':')) for x in element]
                            keys = element_rend[0::2]
                            values = element_rend[1::2]
                            element_dict = dict(zip(keys, values))
                            f.writerow([element_dict['Analysis date'].strip('\n ')[0:19],
                                        items['RequestURL'],items['IPAddress'],
                                        items['CountryCode'],"ASN" + str(items['ASN']),
                                        element_dict['SHA256'],element_dict['SHA1'],items['MD5'],
                                        element_dict['File size'][0:9].strip(' ').strip('('),
                                        element_dict['File name'],element_dict['File type'],
                                        str(data["positives"]) + '%', data["permalink"]])
        time.sleep(16)


def main():
    rss_feed = 'http://malc0de.com/rss/'
    the_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = os.path.join("Product/",
                                "VirusTotal-Report-Less-Than-15-Percent-Detection-Rate" + '-' + the_date + '.csv')
    f = open(csv_filename, "wb+")
    w = csv.writer(f)
    w.writerow(["Scan Date","RequestURL","IPAddress","CountryCode",
                "ASN","SHA256","SHA1","MD5","File Size","File Name",
                "File Type","AV Detection Rate","VirusTotal Report Link"])
    f.close()
    virusTotalTest(csv_filename, rss_feed)

if __name__ == '__main__':
    main()