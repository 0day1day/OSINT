import re
from cymru.bogon.dns import DNSClient as bogon

regex_dict = {"Email": '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
              "Phone": '^(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',
              "IPAddress": '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'}
RegexFactory = type('RegexFactory', (), regex_dict)
obj = RegexFactory()


def regexFactory(object_name, twitter_tweet):
    search_parameter = re.compile(r'%s' % object_name, re.IGNORECASE)
    return search_parameter.findall(twitter_tweet)


def bogon_check(ip_address):
    client = bogon()
    return_dict = client.lookupmany_dict(ip_address, 'IP')
    return return_dict.values()[0]

tweet_en = "this is tweet with an IP Address in the tweet. 0.0.0.0"
cull_ipaddress = regexFactory(obj.IPAddress, tweet_en)
print(bogon_check(cull_ipaddress))