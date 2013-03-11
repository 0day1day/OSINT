

import requests


def get_following_ids(twitter_user_name):
    requestUrl = "https://api.twitter.com/1/friends/ids.json?cursor=-1&screen_name=" + twitter_user_name
    r1 = requests.get(requestUrl)
    print requestUrl
    data = r1.json()
    for items in data['ids']:
        yield items


def main():
    for ids in get_following_ids("AnonymousIRC"):
        print ids


if __name__ == '__main__':
    main()