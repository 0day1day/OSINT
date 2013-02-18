__date__ = "Nov 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import json, requests, csv, datetime, daemon, time
from apiclient.discovery import build

def twitter_searchUrl(twitterSearchSpace_filename):
    """Iterate through the twitterSearchSpace file"""
    for element in open(twitterSearchSpace_filename):
        yield(element)

def google_trans(element_list, src_lang):
    """Call google translate API to translate non-English based Tweets"""
    service = build('translate', 'v2', developerKey='AIzaSyCMNKNNuCoLoL6ZtVJvZWUsUce-lMXLoqQ')
    return service.translations().list(source=src_lang, target="en", q=element_list).execute()

def grabTwitterTopics(search_url, csv_filename, src_lang, country_name):
    """Process Top Ten Trending Non-English Language Based Tweets by WOEID"""
    f = csv.writer(open(csv_filename, "ab+"))
    request_urlGet = requests.get(search_url)
    if '200' in str(request_urlGet.status_code) and 'json' in (request_urlGet.headers['content-type']):
        data = json.loads(request_urlGet.text)
        data_list = data[0]["trends"]
        element_list = []
        for element in data_list:
            if src_lang != "en":
                name = google_trans(element['name'], src_lang)
            else:
                name = element['name']
            element_list.append({'name': name, 'url': element['url']})
        element_list.sort()
        
        key_list = []
        for datadict in element_list:
            curkey = datadict.get('name')
            if curkey not in key_list:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if src_lang != "en":
                    topic = datadict['name']['translations'][0]['translatedText'].strip('#').strip(' ').encode('ascii','ignore')
                else:
                    topic = datadict['name'].strip('#').strip(' ').encode('ascii','ignore')
                url = datadict['url'].encode('ascii','ignore')

                f.writerow([current_time,topic,url,country_name])

def processData(element, csv_filename):
    element = element.split(',')
    search_url = element[0].strip('\n')
    country_name = element[1].strip('\n')
    src_lang = element[2].strip('\n')
    

    grabTwitterTopics(search_url, csv_filename, src_lang, country_name)

def main():
    """Execute process every hour"""
    the_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "culled_product/Twitter-Top-Trending" + '-' + the_date + '.csv'
    f = open(csv_filename,"wb+")
    w = csv.writer(f)
    w.writerow(["Time Observed","Trend Name","URL Request","Country"])
    f.close()
    twitterSearchSpace_filename = "twitterSearchSpace.csv"
    
    for element in twitter_searchUrl(twitterSearchSpace_filename):
        processData(element, csv_filename)
    time.sleep(3600)

if __name__ == '__main__':
    with daemon.basic_daemonize():
        main()
