# -*- coding: utf-8 -*-

"""Pull down malc0de recent hashes - compare to VirusTotal API to determine if malc0de sample has low detection rate"""


import requests, re
from bs4 import BeautifulSoup

def extractlinks(html):
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        links.append(a['href'])
    for element in links:
        yield element

def malcode():
    for i in range(1, 10):
        request_Url = "http://malc0de.com/database/?&page=" + str(i)
        r = requests.get(request_Url)
        for item in extractlinks(r.text):
            if 'search' in item:
                line = item.split('=')[1]
                ipsrch = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                data_list = []
                if ipsrch.findall(line) != None:
                    data_list.append(ipsrch.findall(line))
                    a_list = []
                    print(data_list)
                    for item in sorted((set(item) for item in data_list), key=len, reverse=True):
                        if not any(item.issubset(Q) for Q in a_list):
                            a_list.append(item)
                            for element in a_list:
                                yield(element)

for hash_val in malcode():
    print(hash_val)
