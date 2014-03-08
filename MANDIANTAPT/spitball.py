__date__ = "03082014"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "0.0.7"
__maintainer__ = "AlienOne"
__email__ = "ali3n0ne@alienone.org"
__status__ = "Prototype"


import requests
import csv
from pandas import DataFrame


"""
Returns list dict objects following format:
===

{'LatLon': ['1.3667', '103.8000'], 'Locale': 'Singapore', 'ASN IP': '54.254.124.68', 'ASN': '38895', 'FQDN': ['www.microsoft-update-info.com', 'nh.microsoft-update-info.com', 's.microsoft-update-info.com', 'e.microsoft-update-info.com', 'microsoft-update-info.com']}
"""


def getData():
    """Get CSV Mandiant Data Set - output list data structure"""
    response = requests.get("https://raw.github.com/alienone/OSINT/master/MANDIANTAPT/APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv")
    iterResponse = response.iter_lines()
    next(iterResponse)
    for line in iterResponse:
        yield line.split(',')


def create_nodes(args=list):
    """Create list of dicts - each dict will represent a node"""
    list_dicts = []
    for prodList in getData():
        if len(prodList[0]) != 0:
            dict_object = dict(zip(args, prodList))
            list_dicts.append(dict_object)
    return list_dicts


def clusterData(args, column_name):
    """Leverage Panadas Groupby to cluster nodes by ASN - Then convert resulting DataFrames into list dicts by cluster"""
    gd = DataFrame(create_nodes(args)).groupby(column_name)
    asn_groups = [x[0] for x in gd]
    for asn in asn_groups:
        df = gd.get_group(asn)
        create_dict = [{k: df.values[i][v] for v, k in enumerate(df.columns)} for i in range(len(df))]
        yield create_dict


def normalize_cluster(cluster):
    """Return dicitonary object with value lists"""
    normalized_cluster = {'ASN': [], 'FQDN': []}
    del normalized_cluster['ASN'][:]
    del normalized_cluster['FQDN'][:]
    for node in cluster:
        for k, v in node.items():
            normalized_cluster[k].append(v)
    return normalized_cluster


def get_attributes(asn_str, csv_file):
    """Lookup additional attributes to add to final product"""
    with open(csv_file, 'rb') as fh:
        for item in fh:
            data = item.split(',')
            if asn_str in data:
                    asn_ip = data[2]
                    lat_lon = data[8:10]
                    country = data[4:5]
                    return lat_lon, country, asn_ip


def normalized_nodes(csv_file):
    """Remove duplicates, add additional attributes"""
    results_list = []
    args = ["FQDN", "ASN"]
    column_name = 'ASN'
    for cluster in clusterData(args, column_name):
        results_list.append(normalize_cluster(cluster))
    for node in results_list:
        asn_str = list(set(node['ASN']))[0]
        keys = ['ASN', 'ASN IP', 'FQDN', 'LatLon', 'Locale']
        values = list(set(node['ASN']))[0], get_attributes(asn_str, csv_file)[2], list(set(node['FQDN'])), \
        get_attributes(asn_str, csv_file)[0], \
                 get_attributes(asn_str, csv_file)[1][0]
        dict_obj = dict(zip(keys, values))
        yield dict_obj


def main():
    """Display nodes and write Country, Latitude/Longitude to CSV for D3.js World Map Display"""
    csv_file = "APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv"
    for node in normalized_nodes(csv_file):
        if 'Singapore' in node['Locale']:
            print node


if __name__ == '__main__':
    main()
