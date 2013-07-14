import csv
import requests
import datetime
import time


def getFqdnList(ipAddress, APIKEY, requestUrl):
    parameters = {'ip': ipAddress, 'apikey': APIKEY}
    response = requests.get(requestUrl, params=parameters)
    try:
        responseList = response.json()['resolutions']
        fqdn_list = []
        for item in responseList:
            fqdn_list.append(item['hostname'])
            return fqdn_list
    except KeyError:
        pass


def getData():
    response = requests.get("https://github.com/alienone/OSINT/blob/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "APT-VirusTotal-Enrichment-Product-" + current_time + '.csv'
    APIKEY = 'd706a20a61bbc8e0ad0bc926a2f3b6a8141da312b4bb458806f5d1a3d35a64dd'
    requestUrl = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    with open(csv_filename, 'wt') as f:
        w = csv.writer(f)
        w.writerow(["FQDN","ASN","IP Address","FQDNS","Country_Code","Country_Name","Region_Code","Region_Name","City_Name","Latitude","Longitude","Metro_Code","Area_Code","Time_Zone","Continent_Code",
                    "Postal_Code","Isp_Name","Organization_Name","Domain","As_Number","Netspeed","User_Type","Accuracy_Radius","Country_Confidence","City_Confidence","Region_Confidence","Postal_Confidence"])
    try:
        with open(csv_filename, 'at') as f:
            element_list = []
            for prodList in getData():
                element_list.insert(4, getFqdnList(prodList[2], APIKEY, requestUrl))
                print element_list
                w = csv.writer(f)
                w.writerow(element_list)
                time.sleep(15)
    except IndexError:
        pass


if __name__ == '__main__':
    main()