__date__ = "February 15, 2013"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["AlienOne"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Prototype"

"""Monitor Twitter Real Time Data Stream via a List of keywords"""


import tweetstream
from apiclient.discovery import build


def google_trans(element_list, src_lang):
    """Send Element to Google Translate API - Translate From Source Lang to English"""
    service = build('translate', 'v2', developerKey='AIzaSyBBerCBD8iRTp_EoMNY7nCaSp1GXOPCju8')
    return service.translations().list(source=src_lang, target="en", q=element_list).execute()


def twitterStream(follow_ids, keywords):
    """Watch Twitter RealTime Stream for WatchList Elements"""
    with tweetstream.FilterStream("conmon43wazoo", "ninja789", folow=follow_ids, track=keywords) as stream:
        for tweet in stream:
            try:
                src_lang = tweet['user']['lang']
                if src_lang != "en":
                    if 'web' in tweet['source']:
                        source_platform = tweet['source']
                    else:
                        source_platform = tweet['source'].split('"')[4].split('>')[1].split('<')[0]
                    translatedTweet = google_trans(tweet['text'], src_lang)
                    creation_time = tweet['user']['created_at']
                    geo_location = tweet['geo']
                    coordinates = tweet['coordinates']
                    twitter_id = str(tweet['user']['id'])
                    twitter_screen_name = tweet['user']['screen_name']
                    twitter_proper_name = tweet['user']['name']
                    reply_to_id = tweet['in_reply_to_user_id_str']
                    reply_to_screen_name = tweet['in_reply_to_screen_name']
                    source_lang = tweet['user']['lang']
                    translated_tweet = translatedTweet['translations'][0]['translatedText']
                    keys = ["Ctime", "Geo", "Coordinates", "Platform", "TwitterID", "ScreenName", "ProperName",
                            "ReplyToID", "ReplyToScreenName", "SourceLang", "Tweet"]
                    values = [creation_time, geo_location, coordinates, source_platform, twitter_id, twitter_screen_name,
                              twitter_proper_name, reply_to_id, reply_to_screen_name,
                              source_lang, translated_tweet]
                    twit_dict = dict(zip(keys, values))
                    yield twit_dict
                else:
                    if 'web' in tweet['source']:
                        source_platform = tweet['source']
                    else:
                        source_platform = tweet['source'].split('"')[4].split('>')[1].split('<')[0]
                    creation_time = tweet['user']['created_at']
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
    follow_ids = [365235743, 279390084, 739250522, 358381825, 336683669, 816122462, 225235528, 16589206]
    keywords = ["pastebin"]
    for item in twitterStream(follow_ids, keywords):
        #CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
        cef = 'CEF:0|Twitter RealTime Stream|Twitter|1.0|100|WatchList|1|'
        print(item)

if __name__ == '__main__':
    main()