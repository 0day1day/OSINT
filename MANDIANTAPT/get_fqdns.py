__date__ = "July 14, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Laboratory"


import csv
import requests
import datetime
import time


def getFqdnList(ipAddress, APIKEY, requestUrl):
    try:
        parameters = {'ip': ipAddress, 'apikey': APIKEY}
        response = requests.get(requestUrl, params=parameters)
        responseList = response.json()['resolutions']
        fqdn_list = []
        for item in responseList:
            fqdn_list.append(item['hostname'])
        return fqdn_list
    except KeyError:
        raise KeyError


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def main():
    try:
        APIKEY = 'd706a20a61bbc8e0ad0bc926a2f3b6a8141da312b4bb458806f5d1a3d35a64dd'
        requestUrl = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
        keys = ["FQDN", "ASN", "IP Address", "FQDNS", "Country_Code", "Country_Name", "Region_Code", "Region_Name",
                "City_Name", "Latitude", "Longitude", "Metro_Code", "Area_Code", "Time_Zone", "Continent_Code",
                "Postal_Code", "Isp_Name", "Organization_Name", "Domain", "AsnInfo", "Netspeed", "User_Type",
                "Accuracy_Radius", "Country_Confidence", "City_Confidence", "Region_Confidence","Postal_Confidence"]
        for prodList in getData():
            prodList.insert(3, getFqdnList(prodList[2], APIKEY, requestUrl))
            dict_object = dict(zip(keys, prodList))
            print dict_object
            time.sleep(15)
    except KeyError:
        raise KeyError


if __name__ == '__main__':
    main()