__date__ = "Dec 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"

import argparse, datetime, requests, csv, sys, daemon, time

def maxMind(ipaddress):
    """MaxMind Omni GeoIP REST API"""
    LICENSE = 'YOUR_LICENSE_KEY'
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

def cull_urlData(url_element, file_name):
    """Cull URL Data"""
    request_urlGet = requests.get(url_element)
    if request_urlGet.status_code == 200:
        data = request_urlGet.text
        with open(file_name, 'wt', encoding='utf-8') as f:
            f.write(data)

def tor_routerNodes():
    """Cull Tor Router Nodes"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "Tor-Router-Nodes-" + current_time + '.csv'
    with open(csv_filename, 'wt', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["Node Discovery Date","Node Discovery Time","Node Name","IP Address","Port","Port","Country_Code","Country_Name","Region_Code","Region_Name","City_Name",
                        "Latitude","Longitude","Metro_Code","Area_Code","Time_Zone","Continent_Code","Postal_Code","Isp_Name","Organization_Name","Domain","As_Number","Netspeed",
                        "User_Type","Accuracy_Radius","Country_Confidence","City_Confidence","Region_Confidence","Postal_Confidence"])
    SEARCH_BASE = "http://128.31.0.34:9031/tor/status/all"
    file_name = "tor_router_nodes.txt"
    cull_urlData(SEARCH_BASE, file_name)
    open_file = open(file_name, 'rt', encoding='utf-8')
    for i, line in enumerate(open_file):
        if line.startswith('r'):
            urlDataList = [str(i), line.split()[1:]]
            urlDataDict = dict(zip(urlDataList[0:5], urlDataList[1:]))
            for values in urlDataDict.values():
                try:
                    for elements in maxMind(values[5].strip('\n')):
                        with open(csv_filename, 'at', encoding='utf-8') as f:
                            w = csv.writer(f)
                            w.writerow([values[3],values[4],values[0],values[5],values[6],values[7],elements['country_code'],elements['country_name'],
                                        elements['region_code'],elements['region_name'],elements['city_name'],elements['latitude'],elements['longitude'],
                                        elements['metro_code'],elements['area_code'],elements['time_zone'],elements['continent_code'],elements['postal_code'],
                                        elements['isp_name'],elements['organization_name'],elements['domain'],elements['as_number'],elements['netspeed'],
                                        elements['user_type'],elements['accuracy_radius'],elements['country_confidence'],elements['city_confidence'],
                                        elements['region_confidence'],elements['postal_confidence']])
                except IndexError:
                    return None

def tor_exitNodes():
    """Cull Tor Exit Nodes"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = "Tor-Exit-Node-List-" + current_time + '.csv'
    with open(csv_filename, 'wt', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(["Node Discovery Date","Node Discovery Time","IP Address",
                    "Country_Code", "Country_Name", "Region_Code", "Region_Name", "City_Name",
                    "Latitude", "Longitude", "Metro_Code", "Area_Code", "Time_Zone", "Continent_Code",
                    "Postal_Code", "Isp_Name", "Organization_Name", "Domain", "As_Number", "Netspeed",
                    "User_Type", "Accuracy_Radius", "Country_Confidence", "City_Confidence", "Region_Confidence",
                    "Postal_Confidence"])
    url_list = ["http://exitlist.torproject.org/exit-addresses", "http://exitlist.torproject.org/exit-addresses.new"]
    for url_element in url_list:
        file_name = "tor_exit_nodes.txt"
        cull_urlData(url_element, file_name)
        open_file = open(file_name, 'rt', encoding='utf-8')
        for i, line in enumerate(open_file):
            if line.startswith('ExitAddress'):
                urlDataList = [str(i), line.split()[1:]]
                urlDataDict = dict(zip(urlDataList[0:5], urlDataList[1:]))
                for values in urlDataDict.values():
                    try:
                        for elements in maxMind(values[0].strip('\n')):
                            with open(csv_filename, 'at', encoding='utf-8') as f:
                                w = csv.writer(f)
                                w.writerow([values[1],values[2],values[0],elements['country_code'],elements['country_name'],
                                            elements['region_code'],elements['region_name'],elements['city_name'],elements['latitude'],
                                            elements['longitude'],elements['metro_code'],elements['area_code'],elements['time_zone'],
                                            elements['continent_code'],elements['postal_code'],elements['isp_name'],elements['organization_name'],
                                            elements['domain'],elements['as_number'],elements['netspeed'],elements['user_type'],
                                            elements['accuracy_radius'],elements['country_confidence'],elements['city_confidence'],
                                            elements['region_confidence'],elements['postal_confidence']])
                    except IndexError:
                        return None

def main():
    """Cull Tor Indicators Every 24 Hours"""
    tor_routerNodes()
    tor_exitNodes()
    time.sleep(86400)

if __name__ == '__main__':
    with daemon.basic_daemonize():
        main()