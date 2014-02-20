import csv
import requests


def get_attributes(csv_file):
    with open(csv_file, 'rb') as fh:
        for item in fh:
            data = item.split(',')
            lat_lon = data[8:10]
            country = data[4:5]
            print [lat_lon, country]


def main():
    csv_file = "APT-Maxmind-Enrichment-Product-2013-07-14-09-25-42.csv"
    print get_attributes(csv_file)


if __name__ == '__main__':
    main()