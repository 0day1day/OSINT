__author__ = "AlienOne"
__date__ = "Sept 9, 2012"

"""
Google YoutTube DataAPI Developer Guide
https://developers.google.com/youtube/1.0/developers_guide_python
Requirements Google gdata python library
http://code.google.com/p/gdata-python-client/
Sign Up For a Google YoutTube API Developer KEY
http://code.google.com/apis/youtube/dashboard/
"""

import re, gdata.youtube, gdata.youtube.service, json, httplib2, time

def formatTime(timestamp):
	ts = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
	return time.strftime("%Y-%m-%d:%H:%M:%S", ts)

def shortenUrl(longUrl):
	API_KEY = "AIzaSyCMNKNNuCoLoL6ZtVJvZWUsUce-lMXLoqQ"
	apiUrl = 'https://www.googleapis.com/urlshortener/v1/url'
	headers = {"Content-type": "application/json"}
	data = {"longUrl": longUrl}
	h = httplib2.Http('.cache')
	try:
		headers, response = h.request(apiUrl, "POST", json.dumps(data), headers)
		output = json.loads(response)
		return(output['id'])
	except Exception, e:
		print "unexpected error %s" % e

def PrintEntryDetails(entry):
	print 'Video title: %s' % entry.media.title.text
	print 'Video published on: %s ' % entry.published.text
	print 'Video description: %s' % entry.media.description.text
	print 'Video category: %s' % entry.media.category[0].text
	print 'Video tags: %s' % entry.media.keywords.text
	print 'Video watch page: %s' % entry.media.player.url
	print 'Video flash player URL: %s' % entry.GetSwfUrl()
	print 'Video duration: %s' % entry.media.duration.seconds

	# non entry.media attributes
	#print 'Video geo location: %s' % entry.geo.location()
	print 'Video view count: %s' % entry.statistics.view_count
	#print 'Video rating: %s' % entry.rating.average

	# show alternate formats
	for alternate_format in entry.media.content:
		if 'isDefault' not in alternate_format.extension_attributes:
			print 'Alternate format: %s | url: %s ' % (alternate_format.type, alternate_format.url)

	# show thumbnails
	for thumbnail in entry.media.thumbnail:
		print 'Thumbnail url: %s' % thumbnail.url

def PrintVideoFeed(feed):
	for entry in feed.entry:
		PrintEntryDetails(entry)

def SearchAndPrint(search_terms):
	yt_service = gdata.youtube.service.YouTubeService()
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = search_terms
	query.orderby = 'viewCount'
	query.racy = 'include'
	feed = yt_service.YouTubeQuery(query)
	feed_list = []
	for entry in feed.entry:
		v_title = 'Video title: %s' % entry.media.title.text
		v_date = 'Video published on: %s ' % entry.published.text
		v_filename = 'Video flash player URL: %s' % entry.GetSwfUrl()
		element = [v_date, v_title, v_filename]
		values = element[0:]
		keys = ['Date', 'Title', 'Filename']
		pairs = zip(keys, values)
		feed_list.append(pairs)
	for item in feed_list:
		assert isinstance(item, object)
		yield item

def searchYoutube(search_terms):
	for item in SearchAndPrint(search_terms):
		assert isinstance(item[0][1].split(' ')[3], object)
		timestamp = item[0][1].split(' ')[3]
		assert isinstance(item[2][1].split(' '), object)
		longUrl = item[2][1].split(' ')[4]
		yield formatTime(timestamp), item[1][1].split(':')[1], shortenUrl(longUrl)

# Define Main
def main():
	search_terms = ["AnonymousIRC", "LutzSec", "Nullsec"]
	product_list = []
	for element in search_terms:
		for item in searchYoutube(element):
			product_list.append(item)
	for i in map(lambda x:x[1], sorted(map(lambda tup:[map(int,tup[0][0:10].split('-')),tup], product_list), reverse=True)):
		print(i)

# Main Execution
if __name__ == '__main__':
	main()