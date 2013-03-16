

from pymongo import MongoClient


def mongo_find(db_name, json_key, json_value):
    connect_db = MongoClient(host="localhost", port=27017)
    dbh = connect_db[db_name]
    tweets = dbh.tweets.find({json_key: json_value})
    for tweet in tweets:
        yield tweet


def main():
    db_name = "twitter"
    json_key = 'ID'
    json_value = ['25912403', '14189809', '16076032', '15473574', '14189809', '16076032']
    for twit_id in json_value:
        for tweet in mongo_find(db_name, json_key, twit_id):
            print tweet['ID'], tweet['Tweet'], tweet['mUserId']

if __name__ == '__main__':
    main()