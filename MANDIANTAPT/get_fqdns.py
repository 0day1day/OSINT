import csv
import requests
import datetime
import time


def getFqdnList(ipAddress, APIKEY, requestUrl):
    parameters = {'ip': ipAddress, 'apikey': APIKEY}
    response = requests.get(requestUrl, params=parameters)
    responseList = response.json()['resolutions']
    try:
        fqdn_list = []
        for item in responseList:
            fqdn_list.append(item['hostname'])
            return fqdn_list
    except KeyError:
        pass


def getData():
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Enrichment-Product2013-05-03-12-36-02.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "APT-Enrichment-Product" + current_time + '.csv'
    APIKEY = 'd706a20a61bbc8e0ad0bc926a2f3b6a8141da312b4bb458806f5d1a3d35a64dd'
    requestUrl = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
    with open(csv_filename, 'wt') as f:
        w = csv.writer(f)
        w.writerow(["FQDN","ASN","IP Address","FQDNS","Country_Code","Country_Name","Region_Code","Region_Name","City_Name","Latitude","Longitude","Metro_Code","Area_Code","Time_Zone","Continent_Code",
                    "Postal_Code","Isp_Name","Organization_Name","Domain","As_Number","Netspeed","User_Type","Accuracy_Radius","Country_Confidence","City_Confidence","Region_Confidence","Postal_Confidence"])
    with open(csv_filename, 'at') as f:
        for prodList in getData():
            prodList.insert(4, getFqdnList(prodList[2], APIKEY, requestUrl))
            print prodList
            w = csv.writer(f)
            w.writerow(prodList)
            time.sleep(15)


if __name__ == '__main__':
    main()