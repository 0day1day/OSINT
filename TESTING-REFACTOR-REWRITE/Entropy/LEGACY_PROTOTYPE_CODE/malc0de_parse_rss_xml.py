import feedparser

def getMalUrls(rss_feed):
    getRssFeed = feedparser.parse(rss_feed)
    for items in getRssFeed.entries:
        item = items.summary_detail.value.encode('ascii', 'ignore').split(',')[0].split(' ')[1]
        yield item

def main():
    rss_feed = 'http://malc0de.com/rss/'
    for element in getMalUrls(rss_feed):
        print("http://" + element)

if __name__ == '__main__':
    main()


# get_('http://www.malwaredomainlist.com/hostslist/mdl.xml',malq)
# get_XML_list('http://malc0de.com/rss',malq)

# # TODO: wrap these in a function
# for url in get_URL('http://vxvault.siri-urz.net/URL_List.php'):
#     if re.match('http', url):
#         push_malware_URL(url,malq)
#
# sacourtext=get_URL('http://www.sacour.cn/showmal.asp?month=%d&year=%d' %
#                    (now.month, now.year)).read()
# for url in re.sub('\<[^>]*\>','\n',sacourtext).splitlines():
#     push_malware_URL(url,malq)