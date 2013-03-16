"""
user
favorited => returns True/False
entities => Twitter Mentions Recorded Here
contributors  => mainly returns None
truncated => returns True/False
text => Tweet message
created_at => Date & Time Tweet Messages was created @
retweeted => returns True or False
in_reply_to_status_id_str => None or Something - Mainly returns None
coordinates => Returns None - or Geo Lat/Long Grid Coordinates
in_reply_to_user_id_str => integer twitter id
source => returns application platform utilized to tweet
in_reply_to_status_id => returns mainly None
in_reply_to_screen_name => twitter screen name
id_str => integer twitter id as a string
place => mainly returns None
filter_level => returns mainly "medium"
retweet_count => how many times the tweet has been re-tweeted
geo => mainly returns None
id => twitter id as integer
in_reply_to_user_id => twitter id as integer
"""

import tweetstream

words = ["FBI"]
with tweetstream.FilterStream("JollyJimBob", "delta0!23123", track=words,) as stream:
    for tweet in stream:
        print tweet['geo']