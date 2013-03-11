

import tweetstream
import re
from itertools import chain
from collections import OrderedDict
from nltk.corpus import stopwords


def twitterStream():
    """Watch Twitter RealTime Stream for WatchList Elements"""
    words = ["Top Secret", "Secret Service", "Classified", "Targeted", "Assassination",
             "Kill Program", "NSA", "wire", "CIA", "FBI", "DEA", "DOJ"]
    with tweetstream.FilterStream("JollyJimBob", "delta0!23123", track=words,) as stream:
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


def main():
    file_name = "tweets_dict_output.txt"
    for tweet in twitterStream():
        try:
            if len(tweet['mUserName']) != 0:
                tweet_list = []
                filter_stop_words = set(stopwords.words('english'))
                words_no_punctuation = re.findall(r'\w+', tweet['Tweet'].lower(), flags=re.UNICODE | re.LOCALE)
                for items in words_no_punctuation:
                    filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                    tweet_list.append(filtered_words)
                flat_tweet_list = ' '.join(list(chain.from_iterable(tweet_list)))
                print (tweet['Name'], tweet['mUserName'], flat_tweet_list)
        except KeyError:
            continue
    # for tweet in encode_json():
    #     record_tweets(file_name, tweet)


if __name__ == '__main__':
    main()