import re
from itertools import chain
from collections import Counter
from collections import OrderedDict
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import ConditionalFreqDist
from cPickle import dump
from cPickle import load


def english_word(word_to_test):
    """NLTK test to determine if word is English"""
    if wordnet.synsets(word_to_test):
        return word_to_test
    else:
        pass


def iterate_tweets(file_name):
    f = open(file_name, 'r')
    for tweets in f:
        tweets_no_punctuation = re.findall(r'\w+', tweets, flags=re.UNICODE | re.LOCALE)
        yield tweets_no_punctuation


def iterate_words(file_name, keyword_list):
    """Iterate over Tweet words and filter out common words in multiple languages"""
    f = open(file_name, 'r')
    filter_stop_words = set(stopwords.words('english'))
    for words in f:
        words_no_punctuation = re.findall(r'\w+', words.lower(), flags=re.UNICODE | re.LOCALE)
        for items in words_no_punctuation:
            if len(items) >= 3:
                if english_word(items):
                    for filter_word in keyword_list:
                        if not filter_word.lower() in items:
                            filtered_words = filter(lambda w: not w in filter_stop_words, items.split())
                            yield filtered_words
                        else:
                            pass


def flatten_lists(*args):
    """Flatten a list of lists data structure into a single list"""
    flat_list = list(chain.from_iterable(*args))
    return flat_list


def pickle_words(file_name, pickle_file, keyword_list):
    """Pickle words from filtered Tweets"""
    flat_list = flatten_lists(iterate_words(file_name, keyword_list))
    file_handle = open(pickle_file, "wb")
    dump(flat_list, file_handle)
    file_handle.close()


def pickle_tweets(file_name, pickle_file):
    """Pickle filtered tweets"""
    list_tweets = []
    for tweet in iterate_tweets(file_name):
        list_tweets.append(tweet)
        file_handle = open(pickle_file, "wb")
    dump(list_tweets, file_handle)
    file_handle.close()


def word_freq_count(*args):
    freq_dict = dict(Counter(*args))
    ordered_freq_dict = OrderedDict(sorted(freq_dict.items(), key=lambda by_key: by_key[1]))
    yield ordered_freq_dict.items()


def lexical_diversity(*args):
    word_count = len(*args)
    vocab_size = len(set(*args))
    diversity_score = word_count / vocab_size
    return diversity_score


def modal_analysis(keyword_list, modals_list):
    cfd = ConditionalFreqDist(keyword_list, modals_list)
    return cfd.tabulate(conditions=keyword_list, samples=modals_list)


def main():
    keyword_list = ["Top Secret", "Secret Service", "Classified", "Targeted", "Assassination",
                    "Kill Program", "NSA", "wire", "CIA", "FBI", "DEA", "DOJ", "hackers",
                    "hacker", "exploit code", "Defense", "Intelligence", "Agency"]
    file_name = "tweets_output.txt"
    pickle_words_file = "words.pickle"
    pickle_words(file_name, pickle_words_file, keyword_list)
    pickle_tweets_file = "tweets.pickle"
    pickle_tweets(file_name, pickle_tweets_file)
    words = load(open("words.pickle"))
    tweets = load(open("tweets.pickle"))
    freq_dist = FreqDist(words)
    print tweets
    print("===")
    print("Conducting Frequency and Lexical Diversity Analysis of Twitter Search Space: ")
    print("===")
    print("Number of words within the twitter search space: ")
    print(len(words))
    print("Number of unique words within twitter search space: ")
    print(len(set(words)))
    print("Lexical Diversity of unique words within twitter search space: ")
    print(lexical_diversity(words))
    print("===")
    print("Conducting Native Language Processing Analysis Utilizing Python NLTK")
    print("===")
    print("Top 50 Frequent Words within the Twitter Search Space: ")
    print(freq_dist.keys()[:50])
    print("===")
    print("Bottom 50 Frequent Words within the Twitter Search Space: ")
    print(freq_dist.keys()[-50:])
    print("===")


if __name__ == '__main__':
    main()