__date__ = "Nov 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup", "Adam Reber => ConvertToBytes function"]
__license__ = "GPL"
__version__ = "1.1.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import requests
import re
import time
import feedparser
import daemon
from bs4 import BeautifulSoup
from syslog.syslog_tcp import *


def convertToBytes(data):
    sizes = ["KB", "MB", "GB", "TB"]
    for i, ending in enumerate(sizes):
        if ending in data:
            multiplier = 1024 ** (i + 1)
            data = float(data[0:data.index(ending)].strip())
            return int(data * multiplier)
    else:
        if "B" in data:
            data = float(data[0:data.index("B")].strip())
        return int(data)


def flatten_lists(list_of_lists):
    iteration = iter(list_of_lists)
    for element in iteration:
        if isinstance(element, (list, tuple)):
            for item in flatten_lists(element):
                yield item
        else:
            yield element


def cull_c2(requestUrl):
    request_urlGet = requests.get(requestUrl)
    request_Text = request_urlGet.text + "#behavioural-info"
    soup = BeautifulSoup(request_Text)
    try:
        c2_tcp_connections = soup.find("table", {"id": "behavioural-information"}).find_all("pre")[-2]
        c2_udp_connections = soup.find("table", {"id": "behavioural-information"}).find_all("pre")[-1]
    except (AttributeError, IndexError):
        return

    c2_ip_list = []

    for item in c2_tcp_connections:
        item2 = re.sub("\n", " ", str(item))
        item3 = re.sub(":", " ", item2)
        ip_search = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        c2_ip_list.append(ip_search.findall(item3))

    for item in c2_udp_connections:
        item2 = re.sub("\n", " ", str(item))
        item3 = re.sub(":", " ", item2)
        print(item3.split(' ')[0])
        ip_search = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        c2_ip_list.append(ip_search.findall(item3))
    filtered_list = filter(None, c2_ip_list)

    for element in flatten_lists(filtered_list):
        if element is not None:
            yield element


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
    sock = syslog_tcp_open('127.0.0.1', port=1026)
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
                            analysis_date = element_dict['Analysis date'].strip()[0:19]
                            request_url = items['RequestURL'].strip()
                            ip_address = items['IPAddress'].strip()
                            asn = "ASN" + str(items['ASN']).strip()
                            sha256_hash = element_dict['SHA256'].strip()
                            sha1_hash = element_dict['SHA1'].strip()
                            md5_hash = element_dict['MD5'].strip()
                            file_size = convertToBytes(element_dict['File size'][0:9].strip(' ').strip('('))
                            file_name = str(element_dict['File name'].strip())
                            file_type = element_dict['File type'].strip()
                            av_rate = str(data["positives"]).strip() + '%'
                            vt_link = str(data["permalink"].strip())
                            for c2_item in cull_c2(str(vt_link)):
                                if c2_item is not None:
                                    cef_vt_c2_ip = 'CEF:0|VirusTotal + Malc0de|VirusTotal|1.0|C2|VirusTotal C2|1|' \
                                                   'end=%s request=%s src=%s dst=%s shost=%s cs1=%s cs2=%s ' \
                                                   'cs3=%s fsize=%s fileId=%s fileType=%s cs4=%s ' \
                                                   'requestClientApplication=%s'\
                                                   % (analysis_date, request_url, ip_address, c2_item, asn, sha256_hash,
                                                      sha1_hash, md5_hash, file_size, file_name,
                                                      file_type, av_rate, vt_link)
                                    syslog_tcp(sock, "%s" % cef_vt_c2_ip, priority=0, facility=7)

                            cef_vt = 'CEF:0|VirusTotal + Malc0de|VirusTotal|1.0|Exploit|VirusTotal ' \
                                     'Exploit|1| end=%s ' \
                                     'request=%s src=%s shost=%s cs1=%s cs2=%s cs3=%s fsize=%s fileId=%s ' \
                                'fileType=%s cs4=%s requestClientApplication=%s' \
                                % (analysis_date, request_url, ip_address, asn, sha256_hash,
                                   sha1_hash, md5_hash, file_size, file_name, file_type, av_rate, vt_link)
                            syslog_tcp(sock, "%s" % cef_vt, priority=0, facility=7)

        time.sleep(16)
    syslog_tcp_close(sock)


def main():
    """Run on 12 hour schedule"""
    rss_feed = 'http://malc0de.com/rss/'
    virusTotalTest(rss_feed)
    time.sleep(43200)


if __name__ == '__main__':
    with daemon.DaemonContext():
         main()