# This file is used to build the streaming corpus using TweetCorpus_byTweets class
# Gensim
from TweetCorpus_byTweets import TweetCorpus_byTweets
# Enable logging for gensim - optional
import logging
logging.basicConfig(filename='gensim_faster.log',
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    level=logging.INFO)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

dir = "Tweet_cleaned/"
result_dir = "Result/"

# making object of the class to build the streaming corpus and dictionary to feed to LDA model 
# this is a good resource to understand Gensim in more detail: https://radimrehurek.com/gensim/tut1.html
sentences = TweetCorpus_byTweets(dir+"8-18-2017.txt") # give the name of the file you want to build the corpus of
# vocab = sentences.id2word.token2id
# dictionary = sentences.id2word
sentences.store_corpus(result_dir+"disasterTweets.mm") # saving streaming corpus for later use
sentences.store_dictionary(result_dir+"disasterTweets.dict")  # saving id2word dictionary for later use
