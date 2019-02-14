
import gensim
from collections import defaultdict
from gensim.test.utils import datapath
import numpy as np
from gensim.models.word2vec import Text8Corpus
import os
import ast
import pandas as pd
from gensim.utils import simple_preprocess
from gensim.models.phrases import Phraser
from gensim.models.phrases import Phrases

import pickle

from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['rt', "ain’t", "gonna", "wanna","amp"])


def sent_to_words(sentences):
    tokens = []
    for sentence in sentences:
        tokens = tokens + gensim.utils.simple_preprocess(str(sentence), deacc=True) # deacc=True removes punctuations
    return tokens


dir = "Tweet_cleaned/"

files = os.listdir(dir)

docs = {}
# f_handle = open('vocab_2.txt', 'a')
i = 0
for file in files:
    if file != ".DS_Store":

        data = np.genfromtxt(dir + file, dtype=str, delimiter='\n')

        docs[i] = sent_to_words(data)
        i += 1

        # np.savetxt(f_handle, doc, delimiter=',', fmt='%s')

        # with open(dir+file, 'r') as f:

            # for line in f:
            #     f_handle.write(",".join(sent_to_words(line)))
                # pickle.dump(sent_to_words(line), f_handle)

# f_handle.close()

# vocab = np.genfromtxt('vocab_2.txt', delimiter=',')

# with open('vocab.txt', 'r') as f:
#     for line in f:
#         vocab = vocab + ast.literal_eval(line)


vocab = np.array(docs.values())

bigram = Phrases(vocab, min_count=1, threshold=1)
trigram = Phrases(bigram[vocab], threshold=1)
quadgrams = Phrases(trigram[vocab], threshold=1)

bigram_mod = Phraser(bigram)
trigram_mod = Phraser(trigram)
quadgram_mod = Phraser(quadgrams)


def make_bigrams(texts):
    return np.array([bigram_mod[doc] for doc in texts])


def make_trigrams(texts):
    temp = np.array([trigram_mod[bigram_mod[doc]] for doc in texts])
    return temp


def make_quadgrams(texts):
    temp = np.array([quadgram_mod[trigram_mod[bigram_mod[doc]]] for doc in texts])
    return temp


def remove_stopwords(texts):
    return np.array([[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts])


data_words_nostops = remove_stopwords(vocab)

data_words_bigrams = make_bigrams(data_words_nostops)

data_words_bigrams_trigrams = make_trigrams(data_words_bigrams)

data_words_bigrams_trigrams_quadgrams = make_quadgrams(data_words_bigrams_trigrams)

# print(data_words_bigrams_trigrams_quadgrams)

print(bigram_mod[[u'corpus', u'christi']])

# frequency = defaultdict(int)
# for text in vocab:
#     for token in text:
#         frequency[token] += 1
#
# data_words = [[token for token in doc if frequency[token] > 100] for doc in vocab]
#
#
#
