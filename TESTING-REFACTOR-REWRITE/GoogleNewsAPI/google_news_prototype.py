__date__ = "Nov 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"

import requests, json, csv, datetime, time, daemon
from bs4 import BeautifulSoup

def extractlinks(html):
    """Generic function to extract href links within HTML"""
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    for element in links:
        yield element

def google_news_monitor(csv_filename, search_url):
    """Pull GoogleNews Elements of interest."""
    f = csv.writer(open(csv_filename, "ab+"))
    request_urlGet = requests.get(search_url)
    if '200' in str(request_urlGet.status_code):
        data = json.loads(request_urlGet.text)
        data_list = data['responseData']['feed']['entries']
        for item in data_list:
            for link_item in (extractlinks(item['content'])):
                #print(link_item)
                try:
                    title_item = item['title'].split('-')[0].rstrip()
                    source_item = item['title'].split(' - ')[1].strip()
                    url_link = link_item.split('=')[4]
                    f.writerow([title_item.encode('ascii','ignore'),source_item.encode('ascii','ignore'),url_link.encode('ascii','ignore')])
                except IndexError, e:
                    pass

def main():
    """Execute process every hour"""
    the_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "Google-New-Top-Stories-Monitoring-Report" + '-' + the_date + '.csv'
    f = open(csv_filename, "wb+")
    w = csv.writer(f)
    w.writerow(["Title","News Source","News Source URL"])
    f.close()
    search_url = 'http://goo.gl/XAiwq'
    google_news_monitor(csv_filename, search_url)
    time.sleep(3600)

if __name__ == '__main__':
    with daemon.basic_daemonize():
        main()
