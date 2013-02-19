__date__ = "February 15, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup", "Adam Reber"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"

"""
    Monitor Twitter Real Time Data Stream via a List of Twitter User ID's
    Anonymous       365235743
    OfficialNull    739250522
    OfficialAnonOps 358381825
    AnonIRC         336683669
    wikileaks       16589206

"""


import tweetstream
import time
import socket
from apiclient.discovery import build

CONFIG={}
CONFIG['FACILITY'] = {
    'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
    'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
    'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
    'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
    'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
    }
CONFIG['LEVEL'] = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

def syslog(message, level=CONFIG['LEVEL']['notice'], facility=CONFIG['FACILITY']['daemon'], host='localhost', port=5517):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '<%d>%s' % (level + facility*8, message)
    sock.sendto(data, (host, port))
    sock.close()

def twitterStream(follow_ids):
    """Watch Twitter RealTime Stream for WatchList Elements"""
    with tweetstream.FilterStream("conmon43wazoo", "ninja789", follow=follow_ids) as stream:
        for tweet in stream:
            try:
                    if 'web' in tweet['source']:
                        source_platform = tweet['source']
                    else:
                        source_platform = tweet['source'].split('"')[4].split('>')[1].split('<')[0]
                    tweet_time = tweet['created_at']
                    pattern = '%a %b %d %H:%M:%S +0000 %Y'
                    creation_time = int(time.mktime(time.strptime(tweet_time, pattern))) * 1000
                    geo_location = tweet['geo']
                    coordinates = tweet['coordinates']
                    twitter_id = str(tweet['user']['id'])
                    twitter_screen_name = tweet['user']['screen_name']
                    twitter_proper_name = tweet['user']['name']
                    reply_to_id = tweet['in_reply_to_user_id_str']
                    reply_to_screen_name = tweet['in_reply_to_screen_name']
                    source_lang = tweet['user']['lang']
                    tweet_en = tweet['text']
                    keys = ["Ctime", "Geo", "Coordinates", "Platform", "TwitterID", "ScreenName", "ProperName",
                        "ReplyToID", "ReplyToScreenName", "SourceLang", "Tweet"]
                    values = [creation_time, geo_location, coordinates, source_platform, twitter_id, twitter_screen_name,
                          twitter_proper_name, reply_to_id, reply_to_screen_name,
                          source_lang, tweet_en]
                    twit_dict = dict(zip(keys, values))
                    yield twit_dict
            except KeyError:
                yield KeyError


def main():
    follow_ids = [365235743, 739250522, 358381825, 336683669, 16589206]
    for item in twitterStream(follow_ids):
        #CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
        cef = 'CEF:0|Twitter RealTime Stream|Twitter|1.0|100|WatchList|1|'
        print(item)

if __name__ == '__main__':
    main()