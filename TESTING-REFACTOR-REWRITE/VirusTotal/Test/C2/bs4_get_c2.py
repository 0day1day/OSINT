from netaddr import IPAddress
import pprint
import requests
import re
from bs4 import BeautifulSoup

def exclude_rfc5735_space(address):
    """Exclude RFC 5735 Addresses"""
    ip = IPAddress(address)
    r1 = IPRange('0.0.0.0', '0.255.255.255')
    r2 = IPRange('127.0.0.0', '127.255.255.255')

    if ip not in r1 and ip not in r2:
        return True
    else:
        return False


def exclude_rfc1918_space(address):
    """Exclude RFC 1918 Addresses"""
    result = True
    ip = IPAddress(address)
    for item in dir(ip):
        if item.startswith('is') and 'unicast' not in item:
            result &= not getattr(ip, item)()
    return result


def ip_address_valid(address):
    if exclude_rfc5735_space(address) and exclude_rfc1918_space(address):
        yield address

def grab_ip(requestUrl_Text):
    ip_search = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for ip_address in ip_search.findall(requestUrl_Text):
        if ip_address_valid(ip_address):
            yield ip_address


def get_c2_ip(virus_total_url):
    request_urlGet = requests.get(virus_total_url)
    request_Text = request_urlGet.text + "#behavioural-info"
    for item in grab_ip(request_Text):
        yield item


url = "https://www.virustotal.com/file/8f51bec89429d4b3ddaa7a311a12372441eba16359be3212209cce9b0d508e3e/analysis/1361398687/"
request_urlGet = requests.get(url)
request_Text = request_urlGet.text + "#behavioural-info"
soup = BeautifulSoup(request_Text)
table = soup.find( "table", {"id": "behavioural-information"} )
c2_tcp_connections = soup.find("table", {"id": "behavioural-information"}).find_all("pre")[-2]
c2_udp_connections = soup.find("table", {"id": "behavioural-information"}).find_all("pre")[-1]

for item in c2_tcp_connections:
    print(item)

for item in c2_udp_connections:
    print(item)
