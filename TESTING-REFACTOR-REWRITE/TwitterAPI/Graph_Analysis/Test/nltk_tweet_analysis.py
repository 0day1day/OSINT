import re
from nltk import FreqDist
from nltk.corpus import stopwords
from cPickle import dump
from cPickle import load


def iterate_words(file_name):
    """Iterate over Tweet words and filter out common words in multiple languages"""
    f = open(file_name, 'r')
    filter_stop_words = set(stopwords.words())
    for words in f:
        words_no_punctuation = re.findall(r'\w+', words.lower(),flags=re.UNICODE | re.LOCALE)
        for items in words_no_punctuation:
            if len(items) >= 3:
                filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                yield filtered_words


def flatten_lists(list_of_lists):
    """Flatten a list of lists data structure into a single list"""
    iteration = iter(list_of_lists)
    for element in iteration:
        if isinstance(element, (list, tuple)):
            for item in flatten_lists(element):
                yield item
        else:
            yield element


file_name = "tweets_output.txt"
tweet_lists = []
for item in iterate_words(file_name):
    for element in flatten_lists(item):
        tweet_lists.append(element)
f = open("tweets.pickle", "wb")
dump(tweet_lists, f)
f.close()
words = load(open("tweets.pickle"))
freq_dist = FreqDist(words)
print("===")
print("Conducting Frequency and Lexical Diversity Analysis of Twitter Search Space: ")
print("===")
print("Number of words within the twitter search space: ")
print(len(words))
print("Number of unique words within twitter search space: ")
print(len(set(words)))
print("Lexical Diversity of unique words within twitter search space: ")
print(1.0 * len(set(words)) / len(words))
print("===")
print("Conducting Native Language Processing Analysis Utilizing Python NLTK")
print("===")
print("Top 25 Frequent Words within the Twitter Search Space: ")
print(freq_dist.keys()[:25])
print("===")
print("Bottom 25 Frequent Words within the Twitter Search Space: ")
print(freq_dist.keys()[-25:])
print("===")
