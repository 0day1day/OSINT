__date__ = "Nov 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import requests
import time
import feedparser
import daemon
from bs4 import BeautifulSoup
from syslog.syslog_tcp import *


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


def virusTotalTest(rss_feed):
    """Utilize VirusTotal Public API"""
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
                            analysis_date = element_dict['Analysis date'].strip('\n ')[0:19]
                            request_url = items['RequestURL']
                            ip_address = items['IPAddress']
                            asn = "ASN" + str(items['ASN'])
                            sha256_hash = element_dict['SHA256']
                            sha1_hash = element_dict['SHA1']
                            md5_hash = element_dict['MD5']
                            file_size = element_dict['File size'][0:9].strip(' ').strip('(')
                            file_name = element_dict['File name']
                            file_type = element_dict['File type']
                            av_rate = str(data["positives"]) + '%'
                            vt_link = data["permalink"]
                            cef = 'CEF:0|VirusTotal + Malc0de|VirusTotal|1.0|100|Low AV Detection Rate|1| end=%s' \
                                  ' request=%s src=%s shost=%s cs1=%s cs2=%s cs3=%s fileHash=%s fileId=%s'\
                                  ' filetype=%s cs4=%s requestClientApplication=%s' % (analysis_date, request_url,
                                  ip_address, asn, sha256_hash,
                                  sha1_hash, md5_hash, file_size,
                                  file_name, file_type, av_rate, vt_link)
                            sock = syslog_tcp_open('127.0.0.1', port=1026)
                            syslog_tcp(sock, "%s" % cef, priority=0, facility=7)
                            time.sleep(0.01)
                            syslog_tcp_close(sock)
        time.sleep(16)


def main():
    rss_feed = 'http://malc0de.com/rss/'
    virusTotalTest(rss_feed)

if __name__ == '__main__':
    with daemon.basic_daemonize():
        main()