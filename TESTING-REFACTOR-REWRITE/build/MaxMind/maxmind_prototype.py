# -*- coding: utf-8 -*-
'''
FileName        maxmind_prototype.py
Description     Feed list IP Addresses to MaxMind GeoIP WebService - return Geo IP data
Author          AlienOne
Date            11/20/2012
Time            01:40:06
Version         0.1
Usage           python maxmind_prototype.py
Notes           GeoIP Query Prototype
Python_Version  3.2.3
'''

import argparse
import csv
import requests
import sys

LICENSE = 'LICENSE'
file_name = 'ip_list'


def list_IPaddrs(file_name):
    """Iterate and return ip address from list of ip addresses"""
    open_file = open(file_name, 'r')
    for line in enumerate(open_file):
        yield line[1].strip('\n')

def maxMind(LICENSE):
    fields = ['country_code', 'country_name', 'region_code', 'region_name', 'city_name',
              'latitude', 'longitude', 'metro_code', 'area_code', 'time_zone', 'continent_code',
              'postal_code', 'isp_name', 'organization_name', 'domain', 'as_number', 'netspeed',
              'user_type', 'accuracy_radius', 'country_confidence', 'city_confidence', 'region_confidence',
              'postal_confidence', 'error']
    for ipaddress in list_IPaddrs(file_name):
        parser = argparse.ArgumentParser(description='MaxMind Omni web service client')
        parser.add_argument('--license', default='LICENSE')
        parser.add_argument('--ip', default=ipaddress)
        args = parser.parse_args()
        payload = {'l': args.license, 'i': args.ip};
        response = requests.get('http://geoip.maxmind.com/e', params=payload)
        if response.status_code != requests.codes.ok:
            sys.stderr.write("Request failed with status %s\n" % response.status_code)
            sys.exit(1)
        reader = csv.reader([response.text])
        omni = dict(zip(fields, next(reader)))
        if len(omni['error']):
            sys.stderr.write("MaxMind returned an error code for the request: %s\n" % omni['error'])
            sys.exit(1)
        else:
            print("\nMaxMind Omni data for %s\n\n" % args.ip)
            for (key, val) in omni.items():
                print("  %-20s  %s" % (key, val))

def main():
    maxMind(LICENSE)

if __name__ == '__main__':
    main()
