

import requests
import json
from itertools import chain


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


def main():
    user_name = "AnonymousIRC"
    print list_following(user_name)

if __name__ == '__main__':
    main()