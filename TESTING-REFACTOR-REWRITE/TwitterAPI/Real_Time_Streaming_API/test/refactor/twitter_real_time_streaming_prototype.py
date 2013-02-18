
import tweetstream
from apiclient.discovery import build


def flatten_lists(iterable):
    """Flatten a List of Lists into a single data structure"""
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple)):
            for f in flatten_lists(e):
                yield f
        else:
            yield e


def followers(file_name):
    """Create Flat List of Twitter Follower User ID's"""
    follow = open(file_name, 'r')
    for follower in follow:
        follower_list = []
        follower_list.append(follower.strip('\n'))
        for element in flatten_lists(follower_list):
            yield element


def google_trans(element_list, src_lang):
    """Send Element to Google Translate API - Translate From Source Lang to English"""
    service = build('translate', 'v2', developerKey='AIzaSyBBerCBD8iRTp_EoMNY7nCaSp1GXOPCju8')
    return service.translations().list(source=src_lang, target="en", q=element_list).execute()


def twitterStream(watchlist):
    """Watch Twitter RealTime Stream for WatchList Elements"""
    with tweetstream.FilterStream("Alien1Security", "Tang0!23123", track=watchlist) as stream:
        for tweet in stream:
            for element in tweet:
                print(element)


def main():
    watchlist_one = ["Chinese Hackers", "Russian Mafia", "Syndicate", "HBGary", "Stratfor",
                     "FBI", "CIA", "clandestine", "NSA", "DHS"]
    for item in twitterStream(watchlist_one):
        #CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
        cef = 'CEF:0|Twitter RealTime Stream|Twitter|1.0|100|WatchList|1|'
        print(item)

if __name__ == '__main__':
    main()