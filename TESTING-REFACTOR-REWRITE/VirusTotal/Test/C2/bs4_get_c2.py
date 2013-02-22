
import requests
import re
from bs4 import BeautifulSoup


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
    except AttributeError:
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


def main():
    #requestUrl = "https://www.virustotal.com/file/8f51bec89429d4b3ddaa7a311a12372441eba16359be3212209cce9b0d508e3e/analysis/1361398687/"
    #requestUrl = "https://www.virustotal.com/en/file/561f8bf5d1b6bf32eafc92b91291feb8/analysis/"
    requestUrl = "https://www.virustotal.com/file/a913d2fa305ffca7ce76ab0cccd852d85f38f87929e9471deac1b0252571f5df/analysis/1361542830/"
    for item in cull_c2(requestUrl):
        print item


if __name__ == '__main__':
    main()