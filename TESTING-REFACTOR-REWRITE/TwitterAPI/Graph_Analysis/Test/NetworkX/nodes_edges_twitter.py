

import tweetstream
import re
import requests
import json
from itertools import chain
from collections import OrderedDict
from nltk.corpus import stopwords
from tweetstream import ConnectionError


def get_following_ids(twitter_user_name):
    requestUrl = "https://api.twitter.com/1/friends/ids.json?cursor=-1&screen_name=" + twitter_user_name
    r1 = requests.get(requestUrl)
    if '200' in str(r1.status_code) and 'json' in (r1.headers['content-type']):
        data = json.loads(r1.text)
        for items in data['ids']:
            yield items


def list_following(user_name):
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
                if 'user' in tweet:
                    created_at = tweet['created_at']
                    mentions = tweet['entities']['user_mentions']
                    id_string = tweet['user']['id_str']
                    screen_name = tweet['user']['screen_name']
                    tweet_text = tweet['text']
                    try:
                        if len(mentions) > 0:
                            for record in mentions:
                                user_id = record['id_str']
                                user_name = record['screen_name']
                                user_mentions = "mentions"
                                keys = ['Date', 'ID', 'Name', 'Tweet', 'Mention', 'mUserId', 'mUserName']
                                values = [created_at, id_string, screen_name, tweet_text, user_mentions, user_id, user_name]
                                mentions_dict = dict(zip(keys, values))
                                ordered_mentions_dict = OrderedDict(sorted(mentions_dict.items(),
                                                                           key=lambda by_key: by_key[0]))
                                yield ordered_mentions_dict
                        else:
                            no_mentions = "no_mentions"
                            keys = ['Date', 'ID', 'Name', 'Tweet', 'Mention']
                            values = [created_at, id_string, screen_name, tweet_text, no_mentions]
                            no_mentions_dict = dict(zip(keys, values))
                            ordered_no_mentions_dict = OrderedDict(sorted(no_mentions_dict.items(),
                                                                          key=lambda by_key: by_key[0]))
                            yield ordered_no_mentions_dict
                    except KeyError:
                        raise KeyError
        except ConnectionError:
            raise ConnectionError


def follow_twitter_pods(user_name):
    for tweet in twitterStream(user_name):
        try:
            if tweet['mUserName']:
                tweet_list = []
                filter_stop_words = set(stopwords.words('english'))
                words_no_punctuation = re.findall(r'\w+', tweet['Tweet'].lower(), flags=re.UNICODE | re.LOCALE)
                for items in words_no_punctuation:
                    filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                    tweet_list.append(filtered_words)
                flat_tweet_list = ' '.join(list(chain.from_iterable(tweet_list)))
                print (tweet['Name'], tweet['mUserName'], flat_tweet_list, tweet['Mention'])
            else:
                tweet_list = []
                filter_stop_words = set(stopwords.words('english'))
                words_no_punctuation = re.findall(r'\w+', tweet['Tweet'].lower(), flags=re.UNICODE | re.LOCALE)
                for items in words_no_punctuation:
                    filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                    tweet_list.append(filtered_words)
                flat_tweet_list = ' '.join(list(chain.from_iterable(tweet_list)))
                print(tweet['Name'], tweet['UserName'], flat_tweet_list, tweet['Mention'])
        except KeyError:
            continue


def main():
    user_name = "AnonymousIRC"
    follow_twitter_pods(user_name)

if __name__ == '__main__':
    main()