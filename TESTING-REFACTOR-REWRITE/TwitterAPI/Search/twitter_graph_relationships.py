import re, twitter, json
import networkx as nx

twitter_search = twitter.Twitter(domain="search.twitter.com")
search_results = []

for page in range(1,6):
	search_results.append(twitter_search.search(q="GhostShell", rpp=100, page=page))
json.dumps(search_results, sort_keys=True, indent=1)
tweets = [ r['text'] for result in search_results for r in result['results']]

g = nx.DiGraph()
all_tweets = [ tweet for page in search_results for tweet in page["results"] ]

def get_rt_sources(tweet):
	rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
	return [ source.strip() for tuple in rt_patterns.findall(tweet) for source in tuple if source not in ("RT", "via") ]

for tweet in all_tweets:
	rt_sources = get_rt_sources(tweet["text"])
	if not rt_sources: continue
	for rt_source in rt_sources:
		g.add_edge(rt_source, tweet["from_user"], {"tweet_id" : tweet["id"]})
		for item in g.edges(data=True):
			print(item[0], item[1], item[2]['tweet_id'])


