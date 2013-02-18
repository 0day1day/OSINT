# -*- coding: utf-8 -*-

__author__ = 'AlienOne'

import csv

def gen_twitterSearchSpace(woeid_filename):
    f = csv.writer(open(csv_filename, "wb+"))
    f.writerow(["url","country","lang", "woeid"])
    for values in open(woeid_filename, 'rt'):
        keys = ['country', 'woeid', 'lang']
        dict_struc = dict(zip(keys, values.strip('\n').split(',')))
        f.writerow(["http://api.twitter.com/1/trends/" + dict_struc['woeid'] + ".json",dict_struc['country'],dict_struc['lang'], dict_struc['woeid']])

def twitter_searchUrl(twitterSearchSpace_filename):
    for element in open(twitterSearchSpace_filename):
        yield(element)

# Global Variables
woeid_filename = "woeid.csv"
csv_filename = "twitterSearchSpace.csv"

def main():
#gen_twitterSearchSpace(woeid_filename)
    for url in twitter_searchUrl(csv_filename):
        if url.split(',')[2].strip('\n') != "en":
            print(url.split(',')[2].strip('\n'))

# Main Execution
if __name__ == '__main__':
    main()