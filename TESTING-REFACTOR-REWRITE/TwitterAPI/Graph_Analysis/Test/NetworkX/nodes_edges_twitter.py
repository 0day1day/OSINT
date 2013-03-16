

import tweetstream
import re
import requests
import json
import simplejson
import sys
from daemon import DaemonContext
from pymongo import MongoClient
from itertools import chain
from collections import OrderedDict
from nltk.corpus import stopwords
from tweetstream import ConnectionError


def write_mongo(db_name, element):
    """Write JSON object to MongoDB"""
    try:
        c = MongoClient(host="localhost", port=27017)
    except ConnectionError, e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)
    dbh = c[db_name]
    assert dbh.connection == c
    return dbh.tweets.insert(json.loads(element), safe=True)


class OrderedJsonEncoder( simplejson.JSONEncoder ):
    """Encode ordered dict objects into JSON for write to mongodb"""
    def encode(self, ordered_dict):
        if isinstance(ordered_dict, OrderedDict):
            return "{" + ", ".join([self.encode(k) + ": " + self.encode(v) for (k, v)
                                    in ordered_dict.iteritems()]) + "}"
        else:
            return simplejson.JSONEncoder.encode(self, ordered_dict)


def encode_json(ordered_dict):
    """Encode Ordereddict to JSON"""
    e = OrderedJsonEncoder()
    return e.encode(ordered_dict)


def get_following_ids(twitter_user_name):
    """GET Twitter Id's of Following"""
    requestUrl = "https://api.twitter.com/1/friends/ids.json?cursor=-1&screen_name=" + twitter_user_name
    r1 = requests.get(requestUrl)
    if '200' in str(r1.status_code) and 'json' in (r1.headers['content-type']):
        data = json.loads(r1.text)
        for items in data['ids']:
            yield items


def list_following(user_name):
    """Input Twitter ID's into a flat list data structure"""
    twitter_following_id = []
    for twitter_ids in get_following_ids(user_name):
        twitter_following_id.append(twitter_ids)
    return twitter_following_id


def twitterStream(user_name):
    """Watch Twitter RealTime Stream for WatchList Elements"""
    follow_ids = list_following(user_name)
    with tweetstream.FilterStream("JollyJimBob", "delta0!23123", follow=follow_ids,) as stream:
        try:
            for tweet in stream:
                try:
                    if 'web' in tweet['source']:
                        source_platform = tweet['source']
                    else:
                        source_platform = tweet['source'].split('"')[4].split('>')[1].split('<')[0]
                except KeyError:
                    continue
                if tweet['coordinates'] is None:
                    coordinates = None
                else:
                    coordinates = tweet['coordinates']['coordinates']
                if 'user' in tweet:
                    created_at = tweet['created_at']
                    mentions = tweet['entities']['user_mentions']
                    id_string = tweet['user']['id_str']
                    screen_name = tweet['user']['screen_name']
                    tweet_text = tweet['text']
                    in_reply_to_id = tweet['in_reply_to_user_id_str']
                    in_reply_to_name = tweet['in_reply_to_screen_name']
                    re_tweet_count = tweet['retweet_count']
                    try:
                        if len(mentions) > 0:
                            for record in mentions:
                                user_id = record['id_str']
                                user_name = record['screen_name']
                                user_mentions = "mentions"
                                keys = ['Date', 'ID', 'Platform', 'Coord', 'Name', 'InReplyToId', 'InReplyToName',
                                        'ReTweetCount', 'Tweet', 'Mention', 'mUserId', 'mUserName']
                                values = [created_at, id_string, source_platform, coordinates,
                                          screen_name, in_reply_to_id, in_reply_to_name, re_tweet_count, tweet_text,
                                          user_mentions, user_id, user_name]
                                mentions_dict = dict(zip(keys, values))
                                ordered_mentions_dict = OrderedDict(sorted(mentions_dict.items(),
                                                                           key=lambda by_key: by_key[0]))
                                yield ordered_mentions_dict
                        else:
                            no_mentions = "no_mentions"
                            keys = ['Date', 'ID', 'Platform', 'Coord', 'Name', 'InReplyToId',
                                    'InReplyToName', 'ReTweetCount', 'Tweet', 'Mention']
                            values = [created_at, id_string, source_platform, coordinates,
                                      screen_name, in_reply_to_id, in_reply_to_name,
                                      re_tweet_count, tweet_text, no_mentions]
                            no_mentions_dict = dict(zip(keys, values))
                            ordered_no_mentions_dict = OrderedDict(sorted(no_mentions_dict.items(),
                                                                          key=lambda by_key: by_key[0]))
                            yield ordered_no_mentions_dict
                    except KeyError:
                        raise KeyError
        except ConnectionError:
            raise ConnectionError


def follow_twitter_pods(user_name):
    """Generate Filtered Tweet - Add to Ordered Dict - For NL Analysis"""
    for tweet in twitterStream(user_name):
        try:
            tweet_list = []
            filter_stop_words = set(stopwords.words('english'))
            words_no_punctuation = re.findall(r'\w+', tweet['Tweet'].lower(), flags=re.UNICODE | re.LOCALE)
            for items in words_no_punctuation:
                filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                tweet_list.append(filtered_words)
            flat_tweet_list = ' '.join(list(chain.from_iterable(tweet_list)))
            nlp_entry = {'NLPTweet': flat_tweet_list}
            tweet.update(nlp_entry)
            ordered_tweet = OrderedDict(tweet)
            yield encode_json(ordered_tweet)
        except KeyError:
            continue


def main():
    db_name = "twitter"
    user_name = "AnonymousIRC"
    for tweet in follow_twitter_pods(user_name):
        write_mongo(db_name, tweet)
        print tweet

if __name__ == '__main__':
    #with DaemonContext():
    main()