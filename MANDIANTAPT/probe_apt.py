__date__ = "May 3, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Laboratory"


"""
Dependencies:
==
- OSX -> brew install adns
- Ubuntu -> sudo apt-get -y install adns
- Fedora -> sudo yum -y install adns
- pip install adns-python
- pip install IPy
- pip install dnspython
- pip install git+https://github.com/trolldbois/python-cymru-services.git
"""

import requests
import sys
import argparse
import datetime
import csv
import dns.resolver
from dns.resolver import NXDOMAIN
from dns.resolver import NoAnswer
from dns.resolver import Timeout
from dns.resolver import NoNameservers
from cymru.ip2asn.dns import DNSClient as ip2asn


def getASN(ip_address):
    """Get the ASN Number from the Team Cymru API"""
    client = ip2asn()
    data = client.lookup(ip_address,qType='IP')
    return data.asn


def maxMind(ipaddress):
    """MaxMind Omni GeoIP REST API"""
    LICENSE = 'ZpYqZUlIY4Pi'
    fields = ['country_code', 'country_name', 'region_code', 'region_name', 'city_name',
              'latitude', 'longitude', 'metro_code', 'area_code', 'time_zone', 'continent_code',
              'postal_code', 'isp_name', 'organization_name', 'domain', 'as_number', 'netspeed',
              'user_type', 'accuracy_radius', 'country_confidence', 'city_confidence', 'region_confidence',
              'postal_confidence', 'error']
    parser = argparse.ArgumentParser(description='MaxMind Omni web service client')
    parser.add_argument('--license', default=LICENSE)
    parser.add_argument('--ip', default=ipaddress)
    args = parser.parse_args()
    payload = {'l': args.license, 'i': args.ip};
    response = requests.get('http://geoip.maxmind.com/e', params=payload)
    if response.status_code != requests.codes.ok:
        sys.stderr.write("Request failed with status %s\n" % response.status_code)
        raise SystemExit
    reader = csv.reader([response.text])
    omni = dict(zip(fields, next(reader)))
    if len(omni['error']):
        pass
    else:
        yield omni


def iterateFile(data_file_name):
    """Iterate over elements within a file"""
    for line in data_file_name:
        yield line


def nameLookup(dns_name):
    """Python nslookup implementation"""
    try:
        for ip_address in dns.resolver.query(dns_name):
            if ip_address.to_text() != '0.0.0.0' and ip_address.to_text() != '127.0.0.1':
                yield dns_name, ip_address.to_text()
    except NXDOMAIN:
        pass
    except NoAnswer:
        pass
    except Timeout:
        pass
    except NoNameservers:
        pass


def enrichData(data_file_name):
    """Enrich IP Address With Attribute from Maxmind and Team Cymru API"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "APT-Maxmind-Enrichment-Product-" + current_time + '.csv'
    with open(csv_filename, 'wt') as f:
        w = csv.writer(f)
        w.writerow(["FQDN","ASN","IP Address","Country_Code","Country_Name","Region_Code","Region_Name","City_Name",
                    "Latitude","Longitude","Metro_Code","Area_Code","Time_Zone","Continent_Code","Postal_Code","Isp_Name","Organization_Name","Domain","As_Number","Netspeed",
                    "User_Type","Accuracy_Radius","Country_Confidence","City_Confidence","Region_Confidence","Postal_Confidence"])
    for item in iterateFile(data_file_name):
        for dns_name, ip_address in nameLookup(item):
            try:
                for elements in maxMind(ip_address):
                    asnName = getASN(ip_address)
                    with open(csv_filename, 'at') as f:
                        w = csv.writer(f)
                        w.writerow([dns_name,asnName,ip_address,elements['country_code'],elements['country_name'],
                                    elements['region_code'],elements['region_name'],elements['city_name'],elements['latitude'],elements['longitude'],
                                    elements['metro_code'],elements['area_code'],elements['time_zone'],elements['continent_code'],elements['postal_code'],
                                    elements['isp_name'],elements['organization_name'],elements['domain'],elements['as_number'],elements['netspeed'],
                                    elements['user_type'],elements['accuracy_radius'],elements['country_confidence'],elements['city_confidence'],
                                    elements['region_confidence'],elements['postal_confidence']])
            except IndexError:
                return None


def main():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/mandiant_apt_list.txt")
    iterResponse = response.iter_lines()
    enrichData(iterResponse)

if __name__ == '__main__':
    main()
