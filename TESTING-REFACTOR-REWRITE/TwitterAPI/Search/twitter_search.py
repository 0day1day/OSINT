import twitter, json, cPickle, nltk

twitter_search = twitter.Twitter(domain="search.twitter.com")
search_results = []
for page in range(1,10):
	search_results.append(twitter_search.search(q="AnonymousIRC", rpp=100, page=page))
json.dumps(search_results, sort_keys=True, indent=1)
tweets = [ r['text'] for result in search_results for r in result['results']]


# Frequency Analysis and Lexical Diversity
words = []
for t in tweets:
	words += [ w for w in t.split() ]

# Pickle our Twitter Search Space product
f = open("AnonymousIRC.pickle", "wb")
cPickle.dump(words, f)
f.close()

# Python Natural Language Processing Tool Kit Analysis
words = cPickle.load(open("AnonymousIRC.pickle"))
freq_dist = nltk.FreqDist(words)

print("===")
print("Conducting Frequency and Lexical Diversity Analysis of Twitter Search Space: ")
print("===")
print("Number of words within the twitter search space: ")
print(len(words))
print("Number of unique words within twitter search space: ")
print(len(set(words)))
print("Lexical Diversity of unique words within twitter search space: ")
print(1.0 * len(set(words)) / len(words))
print("Average words per tweet within the twitter search space: ")
print(1.0 * sum([ len(t.split()) for t in tweets ]) / len(tweets))
print("===")
print("Conducting Native Language Processing Analysis Utilizing Python NLTK")
print("===")
print("Top 25 Frequent Words within the Twitter Search Space: ")
print(freq_dist.keys()[:25])
print("===")
print("Bottom 25 Frequent Words within the Twitter Search Space: ")
print(freq_dist.keys()[-25:])
print("===")
