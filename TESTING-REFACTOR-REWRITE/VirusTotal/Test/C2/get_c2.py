import re
import requests


def grab_ip(element):
    ip_search = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    yield ip_search.findall(element)


def get_c2(virus_total_url):
    request_urlGet = requests.get(url)
    request_Text = request_urlGet.text
    for item in grab_ip(request_Text):
        for element in item:
            cef_vt_c2 = 'CEF:0|VirusTotal C2|VirusTotal|1.0|100|VirusTotal C2|1| dst=%s' % \
                        element.encode('ascii', 'ignore')
            yield cef_vt_c2


url ="https://www.virustotal.com/en/file/fac4cb32b035e373ff4748db1e027267e382203b2d2a555aca9915795c4cd0d4/analysis/"
virus_total_url = url + "#behavioural-info"
for item in get_c2(virus_total_url):
    print(item)